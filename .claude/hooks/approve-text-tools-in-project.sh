#!/usr/bin/env bash
# PreToolUse/Bash hook. Approves a command built only from sed, grep, head, tail, wc, and cut
# when every path the command names sits inside the project. Refuses a sed command that also
# assigns a variable, substitutes a command, or reads a heredoc. None of those can match an allow
# rule, and each one costs David a permission prompt.
#
# A command the hook cannot prove safe gets no decision. The normal permission rules then apply,
# and a doubtful command reaches a prompt rather than running unasked.
#
# sed is the BSD sed in /usr/bin, and BSD sed has no `e` command. A `w` command in a sed script
# can still write a file. The path check therefore reads every word, including the script itself.
set -euo pipefail

input="$(cat)"
cmd="$(jq -r '.tool_input.command // ""' <<<"$input")"
cwd="$(jq -r '.cwd // ""' <<<"$input")"
[ -z "$cmd" ] && exit 0
case "$cmd" in
  *sed*|*grep*|*head*|*tail*|*wc*|*cut*) ;;
  *) exit 0 ;;
esac

# Split the command into segments of words. Single quotes, double quotes, and backslashes group
# characters the way the shell groups them. A segment ends at an unquoted ;, &, |, or newline.
segments=()
segment=""
word=""
in_word=0
quote=""
has_expansion=0
has_substitution=0
has_heredoc=0
has_redirect=0

end_word() {
  if [ "$in_word" -eq 1 ]; then
    segment+="$word"$'\x1f'
    word=""
    in_word=0
  fi
}
end_segment() {
  end_word
  if [ -n "$segment" ]; then
    segments+=("$segment")
    segment=""
  fi
}

length=${#cmd}
i=0
while [ "$i" -lt "$length" ]; do
  c="${cmd:i:1}"
  next="${cmd:i+1:1}"
  if [ "$quote" = "'" ]; then
    if [ "$c" = "'" ]; then quote=""; else word+="$c"; fi
  elif [ "$quote" = '"' ]; then
    case "$c" in
      '"') quote="" ;;
      '$') has_expansion=1; [ "$next" = "(" ] && has_substitution=1; word+="$c" ;;
      '`') has_substitution=1; word+="$c" ;;
      '\') word+="$next"; i=$((i + 1)) ;;
      *) word+="$c" ;;
    esac
  else
    case "$c" in
      "'"|'"') quote="$c"; in_word=1 ;;
      '\') word+="$next"; in_word=1; i=$((i + 1)) ;;
      ' '|$'\t') end_word ;;
      ';'|'&'|'|'|$'\n') end_segment ;;
      '$') has_expansion=1; [ "$next" = "(" ] && has_substitution=1; word+="$c"; in_word=1 ;;
      '`') has_substitution=1; word+="$c"; in_word=1 ;;
      '<') [ "$next" = "<" ] && has_heredoc=1; has_redirect=1; word+="$c"; in_word=1 ;;
      '>') has_redirect=1; word+="$c"; in_word=1 ;;
      *) word+="$c"; in_word=1 ;;
    esac
  fi
  i=$((i + 1))
done
end_segment
[ -n "$quote" ] && exit 0
[ "${#segments[@]}" -eq 0 ] && exit 0

has_sed=0
has_assignment=0
only_text_tools=1
for seg in "${segments[@]}"; do
  first="${seg%%$'\x1f'*}"
  case "$first" in
    sed) has_sed=1 ;;
    grep|head|tail|wc|cut) ;;
    *=*) has_assignment=1; only_text_tools=0 ;;
    *) only_text_tools=0 ;;
  esac
done

if [ "$has_sed" -eq 1 ] && { [ "$has_assignment" -eq 1 ] || [ "$has_substitution" -eq 1 ] || [ "$has_heredoc" -eq 1 ]; }; then
  echo "Refused: this sed command also assigns a variable, substitutes a command, or reads a heredoc. None of those match an allow rule, and each one makes David answer a permission prompt. Look up line numbers with a separate plain grep -n. Then send one plain sed -i '' '...' path per call, or use the Edit tool for a change that spans lines." >&2
  exit 2
fi

[ "$only_text_tools" -eq 1 ] || exit 0
[ "$has_expansion" -eq 0 ] && [ "$has_redirect" -eq 0 ] || exit 0

# Every word must stay inside the project. A word naming the project root by its absolute path
# counts as relative. Any other absolute path, a home path, or a parent step leaves the decision
# to the normal permission rules.
for seg in "${segments[@]}"; do
  rest="$seg"
  while [ -n "$rest" ]; do
    w="${rest%%$'\x1f'*}"
    rest="${rest#*$'\x1f'}"
    [ -n "$cwd" ] && w="${w//"$cwd"/.}"
    case "$w" in
      '~'*|/*) exit 0 ;;
    esac
    [[ "$w" =~ (^|/)\.\.(/|$) ]] && exit 0
    [[ "$w" =~ [[:space:]=:,]/ ]] && exit 0
    [[ "$w" =~ [[:space:]]~ ]] && exit 0
  done
done

jq -cn '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "allow",
    permissionDecisionReason: "sed, grep, head, tail, wc, and cut on paths inside the project"
  }
}'
