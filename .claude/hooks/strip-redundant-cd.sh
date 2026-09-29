#!/usr/bin/env bash
# PreToolUse/Bash guard: when Claude prefixes a command with a redundant `cd` into the
# working directory (Bash already runs at the project root), rewrite the command to drop
# the cd and let it proceed through normal permission evaluation. A leading `cd /abs/path`
# defeats every `Bash(<tool>:*)` allow rule (the command no longer *starts with* the tool),
# so the cd doesn't just add a useless step — it forces a permission prompt on commands that
# would otherwise run silently. Stripping it restores the allow-list match. No permission
# decision is emitted, so deny rules (git commit/push/pull) still apply to the cleaned command.
#
# Only rewrites a leading cd whose target is the cwd itself (or `.`, `$PWD`, `$(pwd)`, `` `pwd` ``),
# optionally masked with `2>/dev/null`, followed by `;`, `&&`, or a newline (all unconditional
# separators). Anything else — including `||` — passes untouched.
set -euo pipefail

nl=$'\n'

input="$(cat)"
cmd="$(jq -r '.tool_input.command // ""' <<<"$input")"
cwd="$(jq -r '.cwd // ""' <<<"$input")"
[ -z "$cmd" ] && exit 0

# Trim leading whitespace, then require a leading `cd `.
trimmed="${cmd#"${cmd%%[![:space:]]*}"}"
case "$trimmed" in
  "cd "*) ;;
  *) exit 0 ;;
esac

# First whitespace/;/& -delimited token after `cd ` is the target directory.
rest="${trimmed#cd }"
rest="${rest#"${rest%%[![:space:]]*}"}"
target="${rest%%[[:space:];&]*}"

# Drop one layer of surrounding quotes for the cwd comparison.
tclean="$target"
tclean="${tclean%\"}"; tclean="${tclean#\"}"
tclean="${tclean%\'}"; tclean="${tclean#\'}"

case "$tclean" in
  "$cwd"|"."|"\$PWD"|"\$(pwd)"|'`pwd`') ;;
  *) exit 0 ;;   # cd into somewhere else — a real directory change; leave it alone.
esac

# Everything after the target token: an optional redirection mask, then a `;`/`&&` separator.
after="${rest#"$target"}"
after="${after#"${after%%[![:blank:]]*}"}"
after="${after#2>/dev/null}"
after="${after#>/dev/null 2>&1}"
after="${after#"${after%%[![:blank:]]*}"}"
case "$after" in
  ";"*)    after="${after#;}" ;;
  "&&"*)   after="${after#&&}" ;;
  "$nl"*)  after="${after#"$nl"}" ;; # `cd cwd` on its own line, next command below it
  "")      after="" ;;               # bare `cd cwd` — the whole command is a no-op
  *) exit 0 ;;                       # unrecognized tail (e.g. `||`) — don't risk mangling it
esac

newcmd="${after#"${after%%[![:space:]]*}"}"
[ -z "$newcmd" ] && newcmd="true"    # `cd cwd` alone → harmless no-op

reason="Dropped a redundant \`cd ${tclean}\` — Bash already runs at ${cwd}. Skip the cd (and any 2>/dev/null masking it) and use root-relative paths; the leading cd also defeats the Bash allow-list, which is why these prompt."

jq -cn \
  --arg nc "$newcmd" \
  --argjson ti "$(jq -c '.tool_input' <<<"$input")" \
  --arg r "$reason" \
  '{
     hookSpecificOutput: {
       hookEventName: "PreToolUse",
       updatedInput: ($ti + {command: $nc}),
       additionalContext: $r
     }
   }'
