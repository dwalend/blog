I need a Set with an Index for net.walend.graph.semiring algorithms to work efficiently. I built the original version on Seq and Set in combination, but that's not quite what I mean, and it inflatest the API.

Set extends AbstractSet[A] with Set[A] with GenericSetTemplate[A, HashSet] with SetLike[A, HashSet[A]] with CustomParallelizable[A, ParHashSet[A]] with Serializable . Further, object HashSet extends ImmutableSetFactory[HashSet] with Serializable

So for a Set I need to extend AbstractSet. I just need an immutable set. So that was pretty easy.

Show some code.

Internally there's a Seq and a Set (built from that Seq). The Set gets used for contains(), but the Seq gets used for everything else. In general, I'll be using the Seq so that I can carry around the order of things.

I added an apply() method to get the value at some index, which is the bit that makes all the difference, and a companion object with its apply() method so I can build an IndexedSet from a Seq.

Serializable -- no pain. immutable.Set -- already there. SetLike -- already there. 

GenericSetTemplate[A,IndexedSet] seems happy in the IDE, but has an impenitrable error message:

[error] /Users/dwalend/projects/ScalaGraphMinimizer/src/main/scala/net/walend/graph/IndexedSet.scala:15: overriding method companion in trait GenericTraversableTemplate of type => scala.collection.generic.GenericCompanion[net.walend.graph.IndexedSet];
[error]  method companion in trait Set of type => scala.collection.generic.GenericCompanion[scala.collection.immutable.Set] has incompatible type;
[error]  other members with override errors are: newBuilder
[error] class IndexedSet[A](seq:Seq[A]) extends AbstractSet[A] with GenericSetTemplate[A,IndexedSet] with Set[A] with Serializable  {
[error]       ^
[error] one error found

Back off and come back to that.

Tried ImmutableSetFactory, which requires SetLike with the concrete class. These two are interrelated, but extending SetLike from the class and ImmutableSetFactory from the object compiles.

It looks like CustomParallelizable is going to depend on a new class, ParIndexedSet, with a new complementary object. The class will need to extends ParSet[T] with GenericParTemplate[T, ParHashSet] with ParSetLike[T, ParHashSet[T], HashSet[T]] with Serializable, and the object will need to extend ParSetFactory[ParHashSet] with Serializable. Hit a bit of an unresolved puzzle with empty, and didn't implement all of the methods on the first pass. Lots of ???s




