import pytest

from poetry_analyser.Model import *

test_model = Model()


# Test for short 2-line poem
def test_get_lines01():
    test_model.poem_injection("This is a short poem\nContaining just 2 lines")
    assert test_model.line_dict == {1: "This is a short poem", 2: "Containing just 2 lines"}


# Test for a single line poem
def test_get_lines02():
    test_model.poem_injection("This is a single line poem")
    assert test_model.line_dict == {1: "This is a single line poem"}


# Test for more complex poem with trailing whitespaces
def test_get_lines03():
    test_model.poem_injection("This is a \n more complicated poem \n consisting of irregular line lengths\n and line "
                              "breaks\n ysv")
    assert test_model.line_dict == {1: "This is a", 2: "more complicated poem",
                                    3: "consisting of irregular line lengths", 4: "and line breaks", 5: "ysv"}


# Test for multiple line breaks between lines or stanzas in a poem
def test_get_lines04():
    test_model.poem_injection("This poem will test\n\n\n for multiple line breaks \n\n within a single poem")
    assert test_model.line_dict == {1: "This poem will test", 2: "for multiple line breaks", 3: "within a single poem"}


# Test for empty text or just new lines
def test_get_lines05():
    test_model.poem_injection("\n\n\n\n\n\n\n")
    assert test_model.line_dict == {}


# Test for real poem - Shakespeare's Sonnet 18
def test_get_lines06():
    test_model.poem_injection("""Shall I compare thee to a summer’s day?
Thou art more lovely and more temperate.
Rough winds do shake the darling buds of May,
And summer’s lease hath all too short a date.
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimmed;
And every fair from fair sometime declines,
By chance, or nature’s changing course, untrimmed;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow’st,
Nor shall death brag thou wand'rest in his shade,
When in eternal lines to Time thou grow'st.
So long as men can breathe, or eyes can see,
So long lives this, and this gives life to thee.""")

    assert test_model.line_dict == {1: "Shall I compare thee to a summer’s day?",
                                    2: "Thou art more lovely and more temperate.",
                                    3: "Rough winds do shake the darling buds of May,",
                                    4: "And summer’s lease hath all too short a date.",
                                    5: "Sometime too hot the eye of heaven shines,",
                                    6: "And often is his gold complexion dimmed;",
                                    7: "And every fair from fair sometime declines,",
                                    8: "By chance, or nature’s changing course, untrimmed;",
                                    9: "But thy eternal summer shall not fade,",
                                    10: "Nor lose possession of that fair thou ow’st,",
                                    11: "Nor shall death brag thou wand'rest in his shade,",
                                    12: "When in eternal lines to Time thou grow'st.",
                                    13: "So long as men can breathe, or eyes can see,",
                                    14: "So long lives this, and this gives life to thee."}


# Test for Shakespeare Sonnet 18
def test_get_line_count01():
    test_model.poem_injection("""Shall I compare thee to a summer’s day?
Thou art more lovely and more temperate.
Rough winds do shake the darling buds of May,
And summer’s lease hath all too short a date.
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimmed;
And every fair from fair sometime declines,
By chance, or nature’s changing course, untrimmed;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow’st,
Nor shall death brag thou wand'rest in his shade,
When in eternal lines to Time thou grow'st.
So long as men can breathe, or eyes can see,
So long lives this, and this gives life to thee.""")

    assert test_model.line_count == 14


# Test for no line poem
def test_get_line_count02():
    test_model.poem_injection("")

    assert test_model.line_count == 0


# Test for 2 line poem
def test_get_line_count03():
    test_model.poem_injection("""This is a poem
Consisting of 2 lines""")

    assert test_model.line_count == 2


# Simple rhyming 2-line test
def test_get_rhyme_scheme01():
    test_model.poem_injection("""Hickory dickory dock
The mouse ran up the clock""")

    assert test_model.get_rhyme_scheme() == [1, 1]


# Made up test rhyme scheme (A-A-B-C)
def test_get_rhyme_scheme02():
    test_model.poem_injection("""This is a rhyme
It rhymes with time.
It doesn't rhyme with this.
Nor with this one.""")

    assert test_model.get_rhyme_scheme() == [1, 1, 2, 3]


# Shakespearean Sonnet (A-B-A-B, C-D-C-D, E-F-E-F, G-G)
@pytest.mark.xfail(reason="cmudict too inaccurate for this test to pass - pronunciations missing and doesn't detect "
                          "half-rhyme. "
                          "for instance, cmudict cannot match 'temperate'/'date'. ")
def test_get_rhyme_scheme03():
    test_model.poem_injection("""Shall I compare thee to a summer’s day?
Thou art more lovely and more temperate.
Rough winds do shake the darling buds of May,
And summer’s lease hath all too short a date.

Sometime too hot the eye of heaven shines,
And often is his gold complexion dimmed;
And every fair from fair sometime declines,
By chance, or nature’s changing course, untrimmed;

But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow’st,
Nor shall death brag thou wand'rest in his shade,
When in eternal lines to Time thou grow'st.

So long as men can breathe, or eyes can see,
So long lives this, and this gives life to thee.""")

    assert test_model.get_rhyme_scheme() == [1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6, 8, 8]


# Coupled Rhyme scheme (A-A-B-B)
def test_get_rhyme_scheme04():
    test_model.poem_injection("""The sky is very sunny.
The children are funny.
Under the tree we sit,
But just for a bit.""")

    assert test_model.get_rhyme_scheme() == [1, 1, 2, 2]


# Alternating rhyme scheme (A-B-A-B), longer poem
def test_get_rhyme_scheme05():
    test_model.poem_injection("""The people along the sand
All turn and look one way.
They turn their back on the land.
They look at the sea all day.

As long as it takes to pass
A ship keeps raising its hull;
The wetter ground like glass
Reflects a standing gull

The land may vary more;
But wherever the truth may be—
The water comes ashore,
And the people look at the sea.

They cannot look out far.
They cannot look in deep.
But when was that ever a bar
To any watch they keep?""")

    assert test_model.get_rhyme_scheme() == [1, 2, 1, 2, 3, 4, 3, 4, 5, 6, 5, 6, 7, 8, 7, 8]


# Mono-rhyme rhyme (A-A-A-...)
def test_get_rhyme_scheme06():
    test_model.poem_injection("""It came in a winter’s night,
a fierce cold with quite a bite.
Frosted wind with all its might
sent ice and snow an invite
to layer earth in pure white
and glisten with morning light.""")

    assert test_model.get_rhyme_scheme() == [1, 1, 1, 1, 1, 1]


# Test for no rhyme scheme, AKA Free Verse
def test_get_rhyme_scheme07():
    test_model.poem_injection("""After the Sea-Ship-after the whistling winds;
After the white-gray sails, taut to their spars and ropes,
Below, a myriad, myriad waves, hastening, lifting up their necks,
Tending in ceaseless flow toward the track of the ship:
Waves of the ocean, bubbling and gurgling, blithely prying,
Waves, undulating waves-liquid, uneven, emulous waves,
Toward that whirling current, laughing and buoyant, with curves,
Where the great Vessel, sailing and tacking, displaced the surface;""")

    assert test_model.get_rhyme_scheme() == [1, 2, 3, 4, 5, 6, 7, 8]


# Test for R. Frost 'The Road Not Taken'
@pytest.mark.xfail(reason="cmudict too inaccurate for this test to pass - pronunciations missing and doesn't detect "
                          "half-rhyme. "
                          "for instance, cmudict cannot match 'both'/'undergrowth' or 'hence'/'difference'. ")
def test_get_rhyme_scheme08():
    test_model.poem_injection("""Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.""")

    assert test_model.get_rhyme_scheme() == [1, 2, 1, 1, 2, 4, 5, 4, 4, 5, 6, 7, 6, 6, 7, 8, 9, 8, 8, 9]


# Test for long, complex, chiasmic poem, Dylan Thomas' 'Prologue'
# Realistically this would not be used for Close Reading
@pytest.mark.xfail(reason="cmudict is too inaccurate for this test to pass - pronunciations are not accurate enough. "
                          "for instance, cmudict cannot match up words that 'half rhyme', which are still valid rhymes")
def test_get_rhyme_scheme09():
    test_model.poem_injection("""This day winding down now
At God speeded summer's end
In the torrent salmon sun,
In my seashaken house
On a breakneck of rocks
Tangled with chirrup and fruit,
Froth, flute, fin, and quill
At a wood's dancing hoof,
By scummed, starfish sands
With their fishwife cross
Gulls, pipers, cockles, and snails,
Out there, crow black, men
Tackled with clouds, who kneel
To the sunset nets,
Geese nearly in heaven, boys
Stabbing, and herons, and shells
That speak seven seas,
Eternal waters away
From the cities of nine
Days' night whose towers will catch
In the religious wind
Like stalks of tall, dry straw,
At poor peace I sing
To you strangers (though song
Is a burning and crested act,
The fire of birds in
The world's turning wood,
For my swan, splay sounds),
Out of these seathumbed leaves
That will fly and fall
Like leaves of trees and as soon
Crumble and undie
Into the dogdayed night.
Seaward the salmon, sucked sun slips,
And the dumb swans drub blue
My dabbed bay's dusk, as I hack
This rumpus of shapes
For you to know
How I, a spining man,
Glory also this star, bird
Roared, sea born, man torn, blood blest.
Hark: I trumpet the place,
From fish to jumping hill! Look:
I build my bellowing ark
To the best of my love
As the flood begins,
Out of the fountainhead
Of fear, rage read, manalive,
Molten and mountainous to stream
Over the wound asleep
Sheep white hollow farms


To Wales in my arms.
Hoo, there, in castle keep,
You king singsong owls, who moonbeam
The flickering runs and dive
The dingle furred deer dead!
Huloo, on plumbed bryns,
O my ruffled ring dove
in the hooting, nearly dark
With Welsh and reverent rook,
Coo rooning the woods' praise,
who moons her blue notes from her nest
Down to the curlew herd!
Ho, hullaballoing clan
Agape, with woe
In your beaks, on the gabbing capes!
Heigh, on horseback hill, jack
Whisking hare! who
Hears, there, this fox light, my flood ship's
Clangour as I hew and smite
(A clash of anvils for my
Hubbub and fiddle, this tune
On a toungued puffball)
But animals thick as theives
On God's rough tumbling grounds
(Hail to His beasthood!).
Beasts who sleep good and thin,
Hist, in hogback woods! The haystacked
Hollow farms in a throng
Of waters cluck and cling,
And barnroofs cockcrow war!
O kingdom of neighbors finned
Felled and quilled, flash to my patch
Work ark and the moonshine
Drinking Noah of the bay,
With pelt, and scale, and fleece:
Only the drowned deep bells
Of sheep and churches noise
Poor peace as the sun sets
And dark shoals every holy field.
We will ride out alone then,
Under the stars of Wales,
Cry, multitudes of arks! Across
The water lidded lands,
Manned with their loves they'll move
Like wooden islands, hill to hill.
Hulloo, my prowed dove with a flute!
Ahoy, old, sea-legged fox,
Tom tit and Dai mouse!
My ark sings in the sun
At God speeded summer's end
And the flood flowers now.""")

    assert test_model.get_rhyme_scheme() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                             22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                                             41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 51, 50, 49, 48, 47, 46, 45, 44,
                                             43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25,
                                             24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5,
                                             4, 3, 2, 1]


# Test on poem with repeating rhyme scheme, already tested by get_rhyme_scheme()
def test_stanzafy_rhyme_scheme01():
    test_model.poem_injection("""The people along the sand
All turn and look one way.
They turn their back on the land.
They look at the sea all day.

As long as it takes to pass
A ship keeps raising its hull;
The wetter ground like glass
Reflects a standing gull

The land may vary more;
But wherever the truth may be—
The water comes ashore,
And the people look at the sea.

They cannot look out far.
They cannot look in deep.
But when was that ever a bar
To any watch they keep?""")

    assert test_model.stanzafy_rhyme_scheme() == [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]


# Line with obvious alliteration
def test_get_alliteration01():
    test_model.poem_injection("test text")

    assert test_model.get_alliteration() == [[("test", "text")]]


# Simple tongue twister alliteration
def test_get_alliteration02():
    # import cProfile

    test_model.poem_injection("Peter piper picked a piece of pickled pepper.")
    #
    # with cProfile.Profile() as pr:
    #     test_model.get_alliteration()
    #
    # pr.dump_stats("get_alliteration.prof")

    assert test_model.get_alliteration() == [[("Peter", "piper", "picked"), ("pickled", "pepper")]]


# Mostly alliterative line
def test_get_alliteration03():
    test_model.poem_injection("sweet sally sipped her softdrink")

    assert test_model.get_alliteration() == [[("sweet", "sally", "sipped")]]


# Line with 2 different alliterative groups
def test_get_alliteration04():
    test_model.poem_injection("Cheap chocolate and ripe raisins")

    assert test_model.get_alliteration() == [[("Cheap", "chocolate"), ("ripe", "raisins")]]


# Multiple lines with multiple alliterative groups
def test_get_alliteration05():
    test_model.poem_injection("""A poem possessing multiple lines
                                To test diligent display""")

    assert test_model.get_alliteration() == [[("poem", "possessing")], [("To", "test"), ("diligent", "display")]]


# Multiple lines with multiple alliterative groups
def test_get_alliteration06():
    test_model.poem_injection("""Peter piper picked a piece of pickled pepper
                                But billy batts built a big building""")

    assert test_model.get_alliteration() == [[("Peter", "piper", "picked"), ("pickled", "pepper")],
                                             [("But", "billy", "batts", "built"), ("big", "building")]]


# E. A. Poe 'The Raven' excerpt (3 lines)
def test_get_alliteration07():
    test_model.poem_injection("""Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore—
While I nodded, nearly napping, suddenly there came a tapping""")

    assert test_model.get_alliteration() == [[("upon", "a")], [], [("nodded", "nearly", "napping")]]


# R. Frost 'Birches' excerpt (3 lines)
def test_get_alliteration08():
    test_model.poem_injection("""When I see birches bend to left and right
Across the lines of straighter darker trees,
I like to think some boy's been swinging them.""")

    assert test_model.get_alliteration() == [[("birches", "bend")], [], [("boy's", "been")]]


# J. Harris' Full Peter Piper rhyme (4 lines)
def test_get_alliteration09():
    test_model.poem_injection("""Peter Piper picked a peck of pickled peppers,
A peck of pickled peppers Peter Piper picked;
If Peter Piper picked a peck of pickled peppers,
Where’s the peck of pickled peppers Peter Piper picked?""")

    assert test_model.get_alliteration() == [[("Peter", "Piper", "picked"), ("pickled", "peppers")],
                                             [("pickled", "peppers", "Peter", "Piper", "picked")],
                                             [("Peter", "Piper", "picked"), ("pickled", "peppers")],
                                             [("pickled", "peppers", "Peter", "Piper", "picked")]]


# Denise Rodgers' 'Betty's Room'
def test_get_alliteration10():
    test_model.poem_injection("""There is no clutter cluttered up
more closely, I presume,
than the clutter clustered clingingly
in my friend, Betty's room.

Her mother mutters mawkishly
and fills her with such dread.
She mutters on about the muss
that messes Betty's bed.

At bedtime, Betty bounces all
her objects to the floor.
Each morning, when she wakes up, they
go on her bed once more.

There's papers, pencils, potpourri.
It piques her mother's stress.
She pouts. She plies and yet her cries
do not clean Betty's mess.

There's partly broken plastic toys,
each with a missing part,
some worn and withered whistles, which
are close to Betty's heart.

Old ballet shoes she cannot lose,
and photos of her friends,
a burnt-out fuse, some fruity chews,
a box of odds and ends.

Old magazines and school reports
(the ones that got the A's),
her worn out jeans, some socks to sort,
the programs from three plays.

Each object is an artifact,
a personal antique.
She cannot bear to throw them out;
they make her life unique.

There's feathers, fans, and fairy dolls --
and mother-daughter strife.
Her mother lives for neatness, but,
well, mess is Betty's life.""")

    assert test_model.get_alliteration() == [[("clutter", "cluttered")], [],
                                             [("than", "the"), ("clutter", "clustered")], [],
                                             [("mother", "mutters", "mawkishly")], [], [],
                                             [("Betty's", "bed")],
                                             [("bedtime", "Betty", "bounces")], [], [], [],
                                             [("papers", "pencils", "potpourri")], [], [], [], [], [],
                                             [("withered", "whistles", "which")], [],
                                             [("shoes", "she")], [], [], [], [], [],
                                             [("some", "socks")], [], [], [], [], [],
                                             [("feathers", "fans")], [], [], []]


# Simple one-line caesura using '-'
def test_get_caesura01():
    test_model.poem_injection("This is a line - broken by caesura.")

    assert test_model.get_caesura() == [[1, "This is a line |-| broken by caesura."]]


# Simple 1-line caesura using ','
def test_get_caesura02():
    test_model.poem_injection("To be or not to be, that is the question.")

    assert test_model.get_caesura() == [[1, "To be or not to be |,| that is the question."]]


# 2-line caesura with multiple caesura symbols
def test_get_caesura03():
    test_model.poem_injection("""The mud and leaves in the mauled lane
                                smelled sweet, like blood. Birds had died or flown...""")

    assert test_model.get_caesura() == [[2, "smelled sweet |,| like blood |.| Birds had died or flown..."]]


# Line with no caesura
def test_get_caesura04():
    test_model.poem_injection("No caesura here")

    assert test_model.get_caesura() == []


# Multiple lines and multiple caesuras
def test_get_caesura05():
    test_model.poem_injection("""Lilac, locust, and roses, perfuming
                                East End, West End, wondrously blooming
                                From mother earth.""")

    assert test_model.get_caesura() == [[1, "Lilac |,| locust |,| and roses |,| perfuming"],
                                        [2, "East End |,| West End |,| wondrously blooming"]]


# Testing that apostrophe doesn't test as a caesura
def test_get_caesura06():
    test_model.poem_injection("""This isn't a caesura but it might come up as one.""")

    assert test_model.get_caesura() == []


# 2/3 enjambing lines (source:https://literaryterms.net/enjambment/)
def test_get_enjambment01():
    test_model.poem_injection("""We were running
                                to find what had happened
                                beyond the hills.""")

    assert test_model.get_enjambment() == [1, 2]


# 2/3 enjambing lines (source:https://literaryterms.net/enjambment/)
def test_get_enjambment02():
    test_model.poem_injection("""The sun hovered above
                                the horizon, suspended between
                                night and day.""")

    assert test_model.get_enjambment() == [1, 2]


# 0/3 enjambing lines (source:https://literaryterms.net/enjambment/)
def test_get_enjambment03():
    test_model.poem_injection("""I finished my day.
                                I went home on the highway.
                                I ate dinner and went to sleep.""")

    assert test_model.get_enjambment() == []


# Rita Dove, 'American Smooth' excerpt
def test_get_enjambment04():
    test_model.poem_injection("""We were dancing—it must have
                                been a foxtrot or a waltz,
                                something romantic but
                                requiring restraint, """)

    assert test_model.get_enjambment() == [1, 3]


# R. M. Rilke, 'Love Song' excerpt
def test_get_enjambment05():
    test_model.poem_injection("""How can I keep my soul in me, so that
                                it doesn’t touch your soul? How can I raise
                                it high enough, past you, to other things?
                                I would like to shelter it, among remote
                                lost objects, in some dark and silent place
                                that doesn’t resonate when your depths resound.
                                Yet everything that touches us, me and you,
                                takes us together like a violin’s bow,
                                which draws one voice out of two separate strings.
                                Upon what instrument are we two spanned?
                                And what musician holds us in his hand?
                                Oh sweetest song.""")

    assert test_model.get_enjambment() == [1, 2, 4, 5]


# Simple 1-line test using 2 different phones (source:https://literaryterms.net/assonance/)
def test_get_assonance01():
    test_model.poem_injection("""She seems to beam rays of sunshine with her eyes of green.""")

    assert test_model.get_assonance() == [
        [1, ["IY1", "She", "seems", "beam", "green"], ["AH1", "of", "sunshine", "of"]]]


# 1 line multiple phonetic groups (source:https://literaryterms.net/assonance/)
def test_get_assonance02():
    test_model.poem_injection("""I wish there was a way to make her state similar feelings to those of my soul.""")

    assert test_model.get_assonance() == [[1,
                                           ["AY1", "I", "my"],
                                           ["IH1", "wish", "similar"],
                                           ["AH0", "a", "similar"],
                                           ["EY1", "way", "make", "state"],
                                           ["UW1", "to", "to"],
                                           ["OW1", "those", "soul"]
                                           ]]


# 1 line no assonance
def test_get_assonance03():
    test_model.poem_injection("""This line contains no assonance at all.""")

    assert test_model.get_assonance() == []


# Wordsworth, 'Daffodils' excerpt
def test_get_assonance04():
    test_model.poem_injection("""I wandered lonely as a cloud
                                That floats on high o‘er vales and hills,
                                When all at once I saw a crowd,
                                A host, of golden daffodils;
                                Beside the lake, beneath the trees,
                                Fluttering and dancing in the breeze…""")

    assert test_model.get_assonance() == [[3, ["AO1", "all", "saw"]],
                                          [4, ["AH0", "A", "golden", "daffodils"],
                                           ["OW1", "host", "golden"]],
                                          [5, ["IH0", "Beside", "beneath"],
                                           ["AH0", "the", "the"],
                                           ["IY1", "beneath", "trees"]],
                                          [6, ["IH0", "Fluttering", "dancing", "in"],
                                           ["AH0", "and", "the"]]]


# James Joyce, 'Portrait of the Artist as a Young Man' (prose assonance)
def test_get_assonance05():
    test_model.poem_injection(
        """Soft language issued from their spitless lips as they swished in low circles round and round the field, winding hither and thither through the weeds.""")

    assert test_model.get_assonance() == [[1,
                                           ["AE1", "language", "as"],
                                           ["AH0", "language", "circles", "and", "the", "and", "the"],
                                           ["IH1", "issued", "lips", "swished", "hither", "thither"],
                                           ["IH0", "in", "winding"],
                                           ["AW1", "round", "round"],
                                           ["IY1", "field", "weeds"]]]


# 'My Fair Lady' line, assonant sounds
def test_get_assonance06():
    test_model.poem_injection("The rain in Spain falls mainly on the plane")

    assert test_model.get_assonance() == [[1, ["AH0", "The", "the"], ["EY1", "rain", "Spain", "mainly", "plane"]]]


# Shakespeare, 'Hamlet' excerpt
def test_get_sibilance01():
    test_model.poem_injection("""Sit down awhile;
                                And let us once again assail your ears,  
                                That are so fortified against our story
                                What we have two nights seen.""")

    assert test_model.get_sibilance() == [[1, "Sit"], [2, "us", "once", "assail"], [3, "so", "against", "story"],
                                          [4, "nights", "seen"]]


# Milton, 'Paradise Lost' excerpt
def test_get_sibilance02():
    test_model.poem_injection("""OF MAN’S first disobedience, and the fruit    
                                Of that forbidden tree whose mortal taste    
                                Brought death into the World, and all our woe,    
                                With loss of Eden, till one greater Man    
                                Restore us, and regain the blissful Seat,
                                Sing, Heavenly Muse, that, on the secret top    
                                Of Oreb, or of Sinai, didst inspire    
                                That Shepherd who first taught the chosen seed""")
    # "didst" is problematic as it doesnt appear in cmudict

    assert test_model.get_sibilance() == [[1, "first", "disobedience"], [2, "taste"], [4, "loss"],
                                          [5, "Restore", "us", "blissful", "Seat"], [6, "Sing", "secret"],
                                          [7, "Sinai", "inspire"], [8, "first", "seed"]]


# Simple sibilant line with lots of S's
def test_get_sibilance03():
    test_model.poem_injection("""Seven sorry soldiers stole several of Saddam's settlements""")

    assert test_model.get_sibilance() == [[1, "Seven", "sorry", "soldiers", "stole", "several", "Saddam's",
                                           "settlements"]]


# No sibilance
def test_get_sibilance04():
    test_model.poem_injection("""Nope, none here!""")

    assert test_model.get_sibilance() == []


# Line with multiple S's but not all are sibilant
def test_get_sibilance05():
    test_model.poem_injection("""This line includes several sibilant noises, but with occasional misleading ones!""")
    # Problematic as 'sibilant' not in cmudict!

    assert test_model.get_sibilance() == [[1, "This", "several", "misleading"]]


# Simple anaphora test, The Police 'Every Breath You Take'
# def test_get_anaphora01():
#     test_model.poem_injection("""Every breath you take
#                                 Every move you make
#                                 Every bond you break
#                                 Every step you take
#                                 I’ll be watching you""")
#
#     assert test_model.get_anaphora() == ["Every", 1, 2, 3, 4]
