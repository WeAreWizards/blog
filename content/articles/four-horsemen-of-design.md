Title: The four horsemen of design
Date: 2015-02-26
Short_summary: We explore some formal aspects of good designs.
Category: Misc
Authors: Tom

As a fairly technical agency we do occasionally need help from our
fantastic freelance designer to get a good looking product. You can
read her take on design rules
[here](http://manifesto.co.uk/design-principles-gestalt-white-space-perception/).
<!-- PELICAN_END_SUMMARY -->

But even before talking to our designer there are some rules we can
follow to get a decent-looking and usable design. I know them as *"the
four horsemen of design"*, though I cannot remember where I first
learned this term.

The four horsemen are:

* Alignment
* Repetition
* Proximity
* Contrast

One thing to keep in mind when reading this is that all of the rules
are about a set of elements. A single element in isolation cannot be
aligned, repeated or be close to another element.

If this statement appears false, e.g. in the case of a single word
aligned to the left side of a piece of paper then the set of elements
is not complete: The piece of paper is an element in itself.

## Alignment

To align elements means placing them on a straight line. A very common
example is normal text - like the one in this post. Every row of text
starts along the same vertical, invisible line on the left.

Alignment guides the eye but it also appeals to an inner sense of
order. Unaligned elements look chaotic as the following example
illustrates:

<style>
body { background: #ECECEC; font-family: Montserrat;}
div.fhd-card {
    width: 150px; height: 20px;
    top: 20px;
    left: 20px;
    position: absolute;
    background: #777;
}
div.fhd-card.small {
    width: 100px;
    height: 10px;
}
div.round {
    border-radius: 10px;
}
div.deck {
    font-family: "Montserrat", sans-serif;
    width: 200px;position: relative;
    margin-right: 20px;float: left;
}
div.deck.title {
    margin-top: 20px;
}
div.deck.example {
    height: 140px;
    background: #000;
    margin-bottom: 10px;
}
</style>

<div class="deck title">Aligned</div>
<div class="deck title">Unaligned</div>
<div class="deck example" style="clear: both;">
  <div class="fhd-card small" style="top: 20px;width: 90px;"></div>
  <div class="fhd-card small" style="top: 40px;width: 110px;"></div>
  <div class="fhd-card small" style="top: 60px;width: 120px;"></div>
  <div class="fhd-card small" style="top: 80px;width: 90px;"></div>
  <div class="fhd-card small" style="top: 100px;"></div>
</div>
<div class="deck example">
  <div class="fhd-card small" style="top: 20px;left:83px;width: 90px;"></div>
  <div class="fhd-card small" style="top: 48px;left: 22px;width: 110px;"></div>
  <div class="fhd-card small" style="top: 61px;left: 40px;width: 120px;"></div>
  <div class="fhd-card small" style="top: 80px;left: 46px;width: 90px;"></div>
  <div class="fhd-card small" style="top: 92px;"></div>
</div>

<div style="clear: both;"></div>

Humans are *very* good at picking up even slightly mis-aligned
elements. In the following example I moved one element by only three pixels:

<div class="deck title">Off by three pixels</div>
<div class="deck example" style="clear: both;">
  <div class="fhd-card small" style="top: 20px;width: 90px;"></div>
  <div class="fhd-card small" style="top: 40px;width: 110px;"></div>
  <div class="fhd-card small" style="top: 57px;width: 120px;"></div>
  <div class="fhd-card small" style="top: 80px;width: 90px;"></div>
  <div class="fhd-card small" style="top: 100px;"></div>
</div>

<div style="clear: both;"></div>

Because humans are so good at picking up these small details it is
*very* important to ensure that all elements on a website align.

There can certainly be exceptions to this rule, e.g. to draw the eye
to a specific part of the site, but breaking the alignment rule should
only be done with care and for good reasons!

## Repetition

In everyday speech the word repetition has a slightly negative
connotation. A job might be repetitive, or a person is repeating
themselves.

In design the word repetition is used in the strictest sense: to
repeat elements.

In the following example each element first repeats from top to
bottom, but then we also repeat the entire column of elements a second
time:

<div class="deck title">Repeated elements</div>
<div class="deck example" style="clear: both;">
  <div class="fhd-card small" style="top: 20px;width: 50px;"></div>
  <div class="fhd-card small" style="top: 20px;width: 50px;left: 100px;"></div>
  <div class="fhd-card small" style="top: 40px;width: 50px;"></div>
  <div class="fhd-card small" style="top: 40px;width: 50px;left: 100px;"></div>
  <div class="fhd-card small" style="top: 60px;width: 50px;"></div>
  <div class="fhd-card small" style="top: 60px;width: 50px;left: 100px;"></div>
  <div class="fhd-card small" style="top: 80px;width: 50px;"></div>
  <div class="fhd-card small" style="top: 80px;width: 50px;left: 100px;"></div>
  <div class="fhd-card small" style="top: 100px;width: 50px;"></div>
<div class="fhd-card small" style="top: 100px;width: 50px;left: 100px;"></div>
</div>

<div style="clear: both;"></div>

Repetition is everywhere. When you
[search on Google](https://www.google.com/search?q=on+repeat&ie=utf-8&oe=utf-8#q=repetition+vocabulary)
you will see a block of text repeated ten times per page. The
navigation bar on the
[left side of Wikipedia](http://en.wikipedia.org/wiki/Ada_Lovelace)
repeats navigation elements.

Repetition doesn't just happen in the spacial domain, it also happens
in the temporal domain. If you click around on Wikipedia the content
changes but the layout of the page repeats: Navigation to the left,
text on the right, title on the top.

But why is repetition important? Repetition is a shortcut showing
humans that things are alike. If I can click on the first result in
Google and the layout repeats then it's safe to assume that I can
click on the second, third, etc. result as well.

Breaking the expectation of like things behaving alike can lead to
situations like a kid being confused that a paper magazine
[doesn't react to her touch gestures](https://www.youtube.com/watch?v=OXLKROyVCJ8).

Repetition is not only useful for layout, it is also useful for
colours and shapes. That strays slightly into branding territory
though, so I'm going to omit it ihere.

## Proximity

Proximity explains to the user which elements belong together in a
visual way.

All the elements in close proximity form a new "super" element which
in turn can be aligned and repeated.

The following example is simple but illustrates the point with three
dots making a group, and the group forming a new element that is
repated three times:

<div class="deck title">Which are groups?</div>
<div class="deck title">Probably these.</div>

<div class="deck example" style="clear: both;">
<div class="fhd-card small round" style="top: 20px;width: 10px;"></div>
<div class="fhd-card small round" style="top: 35px;left: 25px;width: 10px;"></div>
<div class="fhd-card small round" style="top: 25px;left: 37px;width: 10px;"></div>

<div class="fhd-card small round" style="top: 80px;left: 70px;width: 10px;"></div>
<div class="fhd-card small round" style="top: 95px;left: 75px;width: 10px;"></div>
<div class="fhd-card small round" style="top: 85px;left: 87px;width: 10px;"></div>

<div class="fhd-card small round" style="top: 50px;left: 130px;width: 10px;"></div>
<div class="fhd-card small round" style="top: 65px;left: 135px;width: 10px;"></div>
<div class="fhd-card small round" style="top: 55px;left: 147px;width: 10px;"></div>
</div>

<div class="deck example">
<div class="fhd-card small round" style="background: #e00;top: 20px;width: 10px;"></div>
<div class="fhd-card small round" style="background: #e00;top: 35px;left: 25px;width: 10px;"></div>
<div class="fhd-card small round" style="background: #e00;top: 25px;left: 37px;width: 10px;"></div>

<div class="fhd-card small round" style="background: #09e;top: 80px;left: 70px;width: 10px;"></div>
<div class="fhd-card small round" style="background: #09e;top: 95px;left: 75px;width: 10px;"></div>
<div class="fhd-card small round" style="background: #09e;top: 85px;left: 87px;width: 10px;"></div>

<div class="fhd-card small round" style="background: #0c0;top: 50px;left: 130px;width: 10px;"></div>
<div class="fhd-card small round" style="background: #0c0;top: 65px;left: 135px;width: 10px;"></div>
<div class="fhd-card small round" style="background: #0c0;top: 55px;left: 147px;width: 10px;"></div>
</div>

<div style="clear: both;"></div>

A slightly more interesting example is the following version of
Google's stylised search results. It's pretty clear that there are two
results on the page, and that the text in each group belongs together:

<div class="deck title">Two results</div>
<div class="deck example" style="clear: both;">
  <div class="fhd-card small" style="top: 20px;width: 140px;height: 7px;"></div>
  <div class="fhd-card small" style="top: 32px;width: 80px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 42px;width: 100px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 52px;width: 70px;height: 5px;"></div>

  <div class="fhd-card small" style="top: 83px;width: 150px;height: 7px;"></div>
  <div class="fhd-card small" style="top: 95px;width: 70px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 105px;width: 60px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 115px;width: 90px;height: 5px;"></div>
</div>

<div style="clear: both;"></div>

The two groups of text create two new super-elements that are aligned to the
left.

## Contrast

A designer creates contrast by picking two ends of a
spectrum. E.g. dark and light, small and large, quiet and loud, close
together and far apart.

Try spotting the important part of the page in the following example:

<div class="deck title">What's important?</div>
<div class="deck example" style="clear: both;">
  <div class="fhd-card small" style="top: 20px;width: 140px;height: 15px;background: #09e;"></div>
  <div class="fhd-card small" style="top: 40px;width: 90px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 50px;width: 90px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 60px;width: 90px;height: 5px;"></div>
</div>

<div style="clear: both;"></div>

The example uses both, colour and size contrast to highlight the
important section.

The following example makes the element at the bottom right stand
out. It might be a contact address, or a button to advance to the next
page:

<div class="deck title">Proximity contrast</div>
<div class="deck example" style="clear: both;">
  <div class="fhd-card small" style="top: 20px;width: 90px;height: 5px;background: #09e;"></div>
  <div class="fhd-card small" style="top: 30px;width: 50px;height: 5px;"></div>
  <div class="fhd-card small" style="top: 40px;width: 70px;height: 5px;"></div>

  <div class="fhd-card small" style="top: 115px;left: 140px; width: 40px;height: 5px;background: #09e;"></div>
</div>

<div style="clear: both;"></div>

Contrast can be used to great effect but it also is the most tricky of
the rules in my experience. That's the point where we go and ask a
designer!

## tl;dr

It is possible to develop a usable and decent-looking design by
following some simple, formal rules; no skill required. Just following
rules won't automatically result in a great design, but it limits the
damage by avoiding design train wrecks.

<div style="clear: both;"></div>
