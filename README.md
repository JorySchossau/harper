# Harper Simple Lesson Discovery and Aggregation

[Harper][harper]'s goal is to help people share, find, and remix lessons more easily:

1.  Instead of creating yet another lesson repository or portal,
    Harper helps teachers to make their existing lessons easier to find.

2.  It uses tagging, voting, and direct online annotation
    to provide feedback to lesson creators.

3.  It does not require people to be technically sophisticated
    in order to comment, contribute, and collaborate.

Harper's design is shaped by:

-   The success of RSS for decentralized content syndication.
-   Mike Caulfield's analysis of [Stack Overflow][stack]
    in terms of [choral explanations][choral-explanations].
-   [This list][oer-landmines] of what has been learned from previous open educational resource (OER) projects.

The project is named after [William Rainey Harper][harper-william],
first president of the University of Chicago,
who encouraged universities to offer distance education courses in the 1890s.

I'm grateful to
Mike Caulfield,
Mine Çetinkaya-Rundel,
Neal Davis,
Garrett Grolemund,
Alison Hill,
Alyson Indrunas,
François Michonneau,
Bracken Mosbacker,
Nick Radcliffe,
Raniere Silva,
Alasdair Smith,
Jon Udell,
and David Wiley
for comments.

## Proposal

To make a lesson easier to find and re-use,
authors create a text file called `harper.yml` and put it in the lesson's root directory.
This single-file convention is inspired by the `feed.xml` and `feed.rss` files used for blogging,
and by the `README.md` and `LICENSE.md` files now commonly used in software projects;
we use the name `harper.yml` because some systems use `lesson.yml` for the actual content of the lesson.

`harper.yml` is formatted as YAML and must contain all of the fields shown below:

```
schema: "harper-lite 0.1"
language: xy
title: "The Title of the Lesson"
url: https://where.to.find/lesson
abstract: >
  A single-paragraph summary of the lesson, the shorter the better.
  It can be broken across multiple lines as shown here, and can
  use [Markdown](https://en.wikipedia.org/wiki/Markdown) formatting.
version: "1.3"
contributor:
  - "Some Name <email@address>"
  - "Another Name <their@address>"
package: http://package.url/lesson.zip
license: http://license.url/
requirements:
  some_technology:
  - "package_1"
  - "package_2>=1.2.3.4"
outcomes:
  - "A short sentence."
  - "Another short sentence."
pre:
  - "[A pre-requisite concept](https://simple.wikipedia.org/wiki/some-key)"
  - "[A pre-requisite skill](https://glosario.carpentries.org/some-other-key)"
post:
  - "[An outcome concept](https://glosario.carpentries.org/some-key)"
  - "[An outcome skill](https://simple.wikipedia.org/wiki/some-other-key)"
notes: >
  One or more sentences describing things instructors ought to know, formatted with Markdown.
  For example, the notes could explain how long the lesson usually takes to do.
```

**Notes:**

-   The `schema` field identifies this as Harper-Lite Version 0.1.

-   The `language` field should be an [ISO 639-1 language code][iso-lang].

-   The `title` and `abstract` fields are self-explanatory.

-   The `version` field is the version of the lesson.
    If the lesson is associated with a software package,
    the lesson and package version numbers should match.

-   Contributors do not need to provide email addresses.

-   The `license` value is the URL of the license rather than an abbreviation.
    We will strongly encourage people to point to licenses at <https://opensource.org/>.

-   The `package` field is the URL for the downloadable lesson materials.

-   `requirements` specifies any packages required,
    organized under one sub-key per language,
    using the syntax preferred by that language's default package manager.

-   Learning outcomes should be single sentences, each with an active verb,
    describing something
    [specific, measurable, attainable, relevant, and time-bound][smart].

-   The `pre` field is a list of terms or skills the lesson requires learners to have;
    the `post` field is a list of terms or skills the lesson teaches.
    (We use these names to avoid collision with `requirements`, which here means "software requirements").
    The items under these keys should be keywords, not full explanations;
    we discuss the use of links below.

-   `notes` is for anything else that might be helpful.

> **Why Links?**
>
> Each entry in `pre` and `post` should link to [Wikipedia](https://simple.wikipedia.org/),
> [Glosario](https://glosario.carpentries.org/),
> or some other widely-used repository of definitions.
> This will make search more accurate,
> encourage use of more uniform terminology,
> and help people stitch lessons together:
> if one lesson has a Wikipedia entry as an output
> and another has it as an input,
> Harper can suggest the former as a prerequisite of the latter.

An example of a Harper file is shown below:

```
schema: "harper-lite 0.1"
language: en
title: "Tests of Univariate Normality"
abstract: >
  How can we tell if univariate data is normally distributed?
  This lesson describes two tests and explains the strengths and weaknesses of each.
version: "1.3.1"
contributor:
  - "Walter Bishop <w.bishop@fringe.tv>"
package: http://stats.fringe.tv/stats454/normality/stats454-normality.zip
license: https://creativecommons.org/licenses/by-nc/4.0/
requirements:
  R:
  - "nickr (>=1.2.3)"
outcomes:
  - "Describe the 68-95-99.7 rule and explain why it works and when it fails."
  - "Describe and apply the Shapiro-Wilk test for normality of univariate data."
pre:
  - "[Normal distribution](https://simple.wikipedia.org/wiki/Normal_distribution)"
  - "[Quantiles](https://glosario.carpentries.org/en/#quantile)"
  - "[Statistical power](https://en.wikipedia.org/wiki/Power_of_a_test)"
  - "Install R package"
post:
  - "[68/95/99.7 rule](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule)"
  - "[Shapiro-Wilk test](https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test)"
  - "`quantile` function in R"
notes: >
  This material was originally developed for a class on real-world data for
  seniors and graduate students in statistics, then modified for delivery in
  conference workshops.  The Shapiro-Wilk material has only been used a couple
  of times, and needs more exercises.
```

## Usage

Harper supports collaboration with a voting mechanism like [Stack Overflow][stack]'s,
using subject headings drawn from lessons as terms:

1.  An author registers a lesson by providing the URL to its Harper file,
    just as someone can register a blog by providing a URL to an aggregator.

2.  The site extracts data from the file
    and displays the lesson under each of `teaches` headings
    to make it easier to find.

3.  When someone views the page for a keyword,
    they can provide comments on the lessons that appear there and vote them up or down.
    This means that a single lesson could appear as the top "answer" for one keyword
    and the third "answer" to another.

To save people from having to write YAML,
Harper provides an interactive upload mode.
After providing a URL for a lesson,
the author is walked through an online form
that asks for the information needed by a `harper.yml` file.
Harper saves that information and gives it back to the author
to download and add to the lesson.
We still require that the Harper file be in the lesson's root directory as a check on authenticity:
allowing people to describe lessons created by other people opens up too many opportunities for abuse.

## Scenarios

### How does an instructor find a lesson?

1. Maya does a DuckDuckGo search for the word "lesson" and the keywords she's interested in.
   If we've done our job right,
   the lessons indexed by our site show up near the top of her search,
   just as Stack Overflow answers show up near the top of a search for a technical question.
2. Alternatively,
   Maya comes to our site and does a targeted search for her keywords.

### How does an author register a lesson?

1. Yim creates a directory on their website with a meaningful name that includes a Harper file
   and possibly a zip file containing starter materials (if the lesson's exercises need any).
2. They sign into their account on our site and register the URL of the lesson directory.
3. Our site validates their Harper file.

As noted above,
we don't allow people to register lessons that they don't control,
i.e.,
they have to be able to add `harper.yml` to the lesson's website
in order for us to accept the registration.

> **Vocabulary**
>
> Harper does some fuzzy matching to suggest rewording of terms
> to match ones in lessons that are already registered.
> The term "[folksonomy][folksonomy]" seems to have lost its luster,
> but encouraging convergence on a shared vocabulary is crucial to making Harper work.

### How does someone ask for a lesson?

Rather than waiting for people to register their own lessons,
we provide a "please register this" workflow:

1.  Paola stumbles across a lesson she finds interesting.

2.  She checks if there's a record of it.

3.  If there isn't,
    but someone before her has expressed an interest,
    we add one to the "want to have" count in our database.

4.  If there isn't any record in our database,
    we scrape the site to get contact info for the lesson's author, Ahmadou.
    We then send Ahmadou a message saying, "Someone is interested in your lesson."

5.  Ahmadou will probably ignore the message,
    but if he responds by creating a record for his lesson,
    we stash that so that future inquiries will resolve
    and notify Paola that the record is now available.
    This workflow serves the triple purpose of attracting more authors,
    not spamming them,
    and ensuring that the record for a lesson comes from someone identified in the lesson's content
    (i.e., probably not a disgruntled former student).

> **Throttling**
>
> We send an author a message the first time someone expresses an interest in their lesson,
> then again when a tenth person expresses an interest,
> and at most one message per year after that.
> All messages include opt-out links.

### How does an author update lesson information?

1.  Prem modifes the `harper.yml` file on their site.
2.  They then sign into their account,
    go to "My Lessons",
    and push the "update" button next to the lesson in question.
3.  Harper reads the latest version of the file and updates its records.

Note that Harper archives old Harper files but not the actual lesson content:
it's an index,
not a repository.

[choral-explanations]: https://hapgood.us/2016/05/13/choral-explanations/
[folksonomy]: https://en.wikipedia.org/wiki/Folksonomy
[harper]: https://github.com/gvwilson/harper
[harper-william]: https://en.wikipedia.org/wiki/William_Rainey_Harper
[iso-lang]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[oer-landmines]: http://third-bit.com/2018/12/02/oer-landmines.html
[smart]: https://ii.library.jhu.edu/2016/07/20/writing-effective-learning-objectives/
[stack]: http://stackoverflow.com
