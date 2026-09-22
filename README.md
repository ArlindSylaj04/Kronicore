# Testfall-Schmiede

A single-file browser tool that turns an existing test-case archive plus a set of Jira
requirements into new, qTest-ready test cases.

**Live page:** https://claude.ai/artifact/GvWiEAPzNXmkjgHrRhGw2m
**Offline:** open `index.html` in any browser — no build step, no server. The only
dependency is SheetJS from cdnjs, used to read `.xlsx`; if your network blocks it the page
says so and CSV still works.

**Standalone build:** on a network that blocks CDNs, build a copy with SheetJS inlined —
one file, no requests at all:

```
python3 tools/build-standalone.py path/to/xlsx.full.min.js Testfall-Schmiede.html
```

Running from disk has a second advantage: the **Save file** buttons on the Export stage
produce real files, which the published page's sandbox does not allow.

Everything runs in the browser. No test case, requirement or ticket text is ever sent
anywhere; the only persistence is `localStorage` in your own browser.

---

## Working with it

**Save project / Open project** writes the whole workspace — knowledge base, past
requirements, drafts, module tree, settings — to one `.json` file. `localStorage` is per
browser and per machine; the project file is what lets you work on two releases, hand a
configured knowledge base to a colleague, and survive a cleared browser.

**Re-importing a module updates it** rather than cloning it. Cases are matched on id plus
name, and the import reports how many were new and how many were replaced in place.

**A draft that repeats an archived case is flagged** with a red `≈ TC-204 · 84%` chip.
Genuinely new drafts score well under the threshold — in testing they sat between 6% and
27%, while an identical case scores around 100% — so the chip means something when it
appears. A case carried over from the archive is not flagged against itself.

**Side by side.** Both the chip and the *Compare with TC-…* button open the archived case
and the draft in two columns with a **word-level** diff — red is only on the left, green
only on the right. A line-level diff is no use here: two test cases that differ in one
number look identical in one. It opens for two different questions:

- a *flagged duplicate*, where the buttons are **Keep both** (clears the flag) and
  **Drop the draft** (the archived case already covers it);
- any draft against *the case it was derived from*, which answers "what did the generator
  keep from TF-207, and what did it write itself?" — there is nothing to decide there, so
  those two buttons do not appear.

Steps are lined up by position, so one inserted step colours everything after it, and the
page says so underneath. Fields identical on both sides stay grey.

**The step editor.** Every step row carries move up, move down, duplicate and delete;
deleting and duplicating take an undo snapshot, moving does not because clicking the other
arrow is the undo. Only the one card re-renders, so the list does not jump and the field
you were typing in keeps focus — after a move, focus follows the step.

**Bulk actions.** Tick the drafts you mean, or *Select all shown* to take whatever the
filters are showing. The bar that appears can approve, put back to draft, drop, delete, and
set module, priority, status or type across the selection. Every one of them snapshots
first. The selection lives for the sitting only: it is never written to the project file
and a stage change clears it.

**Bulk actions can be taken back.** Approving everything shown, discarding unapproved
drafts, placing cases in the tree, removing a branch, clearing the archive, forging a new
set of drafts — each takes a snapshot first, and an *Undo* button appears in the header.
One step, which is what these actions need.

**Ctrl + K searches everything** — archived cases by id, name, module or step text,
requirements and their criteria, past requirements, drafts, and the pipeline stages by
name. Arrows move, Enter opens, Esc closes. The index is rebuilt when the counts move, not
on every keystroke, so a knowledge base of several thousand cases is not re-scanned as you
type. Results come in a fixed order of kinds and each kind is capped, so the list never
reshuffles under your finger and one huge archive cannot crowd the rest out.

**A case opens in a drawer**, not instead of the page. Clicking a row of the archive table,
a `≈ TC-…` chip or a search hit slides it in over whatever you were doing, with its health
checklist and steps; Esc or a click outside closes it and the page is where you left it.

**Saved views.** Any combination of the archive's filters — tree node, type, health band,
search text — can be kept under a name and brought back with one click. They travel in the
project file, because a view describes the project rather than the browser.

**The pipeline folds away.** The rail collapses to the step numbers when you want the width,
and remembers that between visits.

**Review scales.** *Group by* requirement, module, technique or review state turns one long
list into folds, each with its counts and a *Select these* button. *Compact* collapses every
draft to its header; open the ones you need. And with the cursor on a card:

| Key | Does |
|---|---|
| `j` `k` or `↓` `↑` | move the cursor, opening a shut group to reach a card |
| `a` | approve or un-approve |
| `x` | drop or restore |
| `o` or `Enter` | fold open or shut |
| `space` | select for a bulk action |
| `/` | jump to the filter box |
| `Ctrl + K` / `Ctrl + S` | search everything / save the project |
| `Esc` | close an overlay, or drop the cursor |

A letter typed into a step is a letter, never a command — the single-key shortcuts stand
down whenever the focus is in a field.

**Every figure is a way into what it counted.** The tiles, the matrix cells, the technique
bars, the gap rows and the requirement rows are all buttons: clicking one opens the stage
that can act on it, filtered to that slice. Review then shows which filter is active as a
removable pill, so a filtered list never looks like the whole list. A draft's requirement
chip opens the ticket; its `≈ TC-…` chip opens the archived case it resembles.

## How many cases a ticket is worth

Eight cases from one ticket is not thoroughness, it is a review queue. The Generate stage
leads with three depths and prints what each would produce for the tickets now loaded,
next to what your own archive spends on a ticket:

| Depth | What it writes |
|---|---|
| **Lean** | one end-to-end case per ticket, plus a negative case only where a criterion asks for one |
| **Balanced** | one case per criterion, the negatives the criteria ask for, and one end-to-end case |
| **Thorough** | everything above plus boundary values and a permission matrix wherever they apply |

The archive figure is the honest anchor: if your project has historically covered a
requirement with three cases, a preset that produces five per ticket is not more coverage,
it is more review. The five switches underneath still work if none of the three fits.

**Removing a ticket removes its test cases.** A ticket and the drafts written for it are
one thing; leaving the drafts behind is how a project ends up counting work that has no
reason to exist. Anything you already approved is your decision, so that survives and the
toast says how many were kept. One undo brings it all back.

## Testing SAP

qTest holds the cases; the thing being tested is usually something else. Set **System under
test** on the Generate stage — or let it be read off your archive — and for an SAP project
the app changes what it considers a finished test case.

**Transaction codes are learned from your own archive**, not guessed. A token counts as a
transaction code when the public SAP reference the app carries knows it, or when it is at
least four characters and reads like one. Three characters is too little to tell a
transaction from a tag — `E2E`, `UAT` and `SIT` all look like one otherwise — so anything
shorter has to be in the reference, which is where `F-02` comes from. Your own ids are
excluded by shape, so `TC-2134` and `BIB-2101` are never mistaken for transactions. The
Knowledge Base stage lists what it found, how often, and how many of them the reference
can name.

**Each ticket gets the angles SAP asks for**, on its own card, offered one at a time rather
than generated in bulk:

| Angle | Why it is a test |
|---|---|
| Authorisation | in SAP the authorisation is part of the function; the same transaction behaves differently per role, and `SU53` names the missing object |
| Organisational level | what works in one company code or plant is often configured differently in the next |
| Document number and follow-on | a posting without a document number you can point at is not tested |
| Message and message type | "an error appears" is not an expected result; type, class and number are |
| Interface | if the document is meant to reach a neighbouring system, the test ends there — IDoc status 53, not before |
| Background processing | dialogue and job are two paths through one function, and the job has a log rather than a screen |
| Output determination | the document is finished when the output reaches the printer, the mail or EDI |
| Create, change, display | a `…01` transaction always comes with its `…02` and `…03` |

An angle only appears when the ticket's own text touches it, and where the ticket names a
transaction the generated steps call it by code. Cases added this way are marked as yours:
regenerating the ticket never replaces them.

`SAP sample` in the header loads an invented wholesaler's SD, MM and FI project so all of
this can be seen without opening a real one.

## Test health


Every case, archived or drafted, carries a score out of 100 and a band — **Excellent**,
**Good**, **Needs review**, **Critical**. It is not a vibe: each point comes from a field
the case either carries or does not.

| Check | Weight | What earns full marks |
|---|---:|---|
| Test steps | 22 | more than one step |
| Expected results | 22 | every step states one; partial credit for a share of them |
| Requirement link | 14 | an issue key to trace back to |
| Duplicate risk | 14 | no archived case with the same name, no close match in the knowledge base |
| Title | 12 | between 12 and 140 characters, so it reads on its own in a run list |
| Precondition | 10 | the starting state is written down |
| Placement | 8 | a module or a path in the tree |
| Step size | 8 | at most 25 steps, no single step over 400 characters |

**A check your project does not use is not counted against anyone.** If fewer than a fifth
of your archived cases carry a precondition, that is a convention, not ten thousand bad
test cases — the check drops out and the remaining weights are rescaled. The same goes for
requirement links and module placement. The card on the Knowledge Base stage says which
checks it skipped and why.

Duplicate risk is measured differently on the two sides, because the cost is different.
An archived case is checked against the other archived names in one pass — cheap, and it
catches the real consolidation problem, the same test written four times under four old
project names. A draft is checked against the full text of every archived case, which is
the expensive comparison and the one worth paying for on a few dozen drafts.

Where it shows:

- **Knowledge Base** — a distribution across the four bands, plus the archive's mean.
  Clicking a band filters the table to it, which is how you find the thousand cases worth
  migrating and the thousand that are not.
- **The archive table** — a `Health` column on every row, the tooltip naming what is
  missing.
- **A single case** — the full checklist, one line per check, each saying what it found.
- **A draft in Review** — the score in the header, and *"3 things this case is still
  missing"* folded open beneath it, so the fix is next to the field that needs it.

## What it writes, and what it copies

It is a scaffolder, not an author, and the app now says so in its own numbers rather than
leaving you to guess.

The analysis runs on import and takes about a millisecond, because it is word statistics
and pattern matching — there is no language model anywhere in this file. **What was read
from your archive** on the Knowledge Base stage is the whole of it: the naming pattern, the
steps your cases repeat and in what share of them, the values your fields carry, the
language, the shape. Everything a generated case inherits comes from that list.

On the sample archive the split comes out like this:

| | |
|---|---|
| steps copied from the archive word for word | 32 of 59 |
| steps taken from an acceptance criterion | 20 |
| steps written by the tool around a criterion | 7 |
| expected results the ticket actually stated | 9 |

So roughly **two steps in three are carried across, one is the criterion rephrased.** That
is the design — your opening and closing steps, your field values and your naming are
exactly what you want repeated — but it is worth seeing rather than assuming.

**Every step carries its mark**, and every card says how many of each it holds:

| Mark | Means |
|---|---|
| `⧉` | copied from the archive word for word, with the case it came from |
| `◆` | taken from the acceptance criterion, with which one |
| `✎` | written by the tool around the criterion |

A card also names its template and its match score, and says outright when that score is
**too weak to borrow its precondition**. A precondition is a claim about the state of the
system: lifting one off a case that is 15% like this requirement states something false
with confidence, which is worse than stating something general and true. Below 30% the tool
writes its own, on both the per-criterion and the end-to-end path.

## The problem it solves

Every release you get a set of Jira stories and you need test cases in qTest for them.
You already have hundreds of test cases from earlier releases — functional, e2e,
regression — sitting in exports with inconsistent columns. Writing the new cases by hand
means re-inventing your own naming pattern, your own standard login/logout steps and your
own field values every single time.

This tool reads all of that out of the archive and applies it to the new requirements.

## The pipeline

| # | Stage | What happens |
|---|-------|--------------|
| 1 | **Knowledge Base** | The test cases you have already written **and the requirements they were written for**, linked by issue key. Any export, any order, any column layout. Also where cases from old qTest projects are placed in the new module tree. |
| 2 | **Convert** | Cases that already exist, written out in another shape. Its own import, so a batch you only want as a Tosca spec never reaches the knowledge base. |
| 3 | **New Requirements** | Import a Jira CSV, XML or REST JSON export for this release. Acceptance criteria are split into individually testable items. |
| 4 | **Match** | Two routes to a template: directly, requirement text against each archived case; and through history, requirement against each **past** requirement, then the cases that covered it. |
| 5 | **Generate** | Each acceptance criterion produces the cases its ISTQB technique calls for. |
| 6 | **Review** | Edit, add or remove steps, approve or drop. Nothing is final until you approve it. |
| 7 | **Coverage** | What the release covers and what it does not, before any of it reaches qTest: a module × technique matrix, the gaps as a list, the technique mix, and an estimated run time. Printable. |
| 8 | **Export** | qTest import CSV, one row per test step, plus a traceability matrix — and/or a Tosca automation spec. |

Those are not eight steps in a line. **Convert is a branch**, not the second thing you do:
it runs 1 → 2 → 6 → 8 and skips everything between. The forge runs 1 → 3 → 4 → 5 → 6 → 7 → 8.
They share the knowledge base at one end and Review and Export at the other, and nothing in
between.

The **Target** decides which files Export writes — qTest manual cases, a Tosca automation
specification, or both from the same drafts. Convert sets it as part of converting, so it
cannot name a file it was not going to write.

## Coverage

The release view, and the one to take into a planning meeting.

- **Module × technique matrix** — cases per module against the ISTQB technique that
  produced them, on a single-hue sequential ramp where the lightest cell is near zero. A
  pale column across every module is a technique the release is not using at all.
- **Gaps** — every acceptance criterion with no test case, listed. Marked with a status
  colour *and* a label, never colour alone.
- **Technique mix** — one measure across categories, so one hue and no legend. It answers
  whether a release is only proving the happy path.
- **Run time** — read from whichever project field holds a duration, averaged across the
  archive and multiplied by the drafts in this release. An order of magnitude, and the page
  says so.

### Traceability

Requirement → acceptance criterion → the case that answers it, open on the page rather
than only in the exported matrix. Each requirement is a fold showing its coverage bar and
case count; opening it lists every criterion with the cases beneath it, each chip carrying
that case's health and opening it in Review.

A criterion with nothing under it is red and carries the two ways of closing it:

- **Generate** forges the cases for that requirement again from the knowledge base.
  Approved drafts and cases you linked by hand survive it — only untouched drafts are
  replaced.
- **Link existing** opens the closest archived cases, ranked, each with its health. Picking
  one carries it into Review whole — steps, precondition, project fields — pinned to that
  criterion, so it counts towards coverage and lands in the exported matrix. It is not
  flagged as a duplicate of itself, and *Undo* takes it back.

Requirements with a hole open by default when there are twelve or fewer; **Expand all**
handles the rest, and printing opens every fold so nothing prints as a bare heading.

## Two routes to a template

Requirement-to-test-case similarity is a weak signal: a requirement is written in the
language of the business, a test case in the language of clicks. Requirement-to-requirement
is much steadier — so once past requirements are loaded and linked, a new ticket can be
answered with *"this is close to BIB-1204, and these are the cases that covered it"*.

The link comes from the archive itself: a qTest export usually carries the issue key each
case was written for, in `Anforderung` or `Test Case Jira Requirement ID`.

Where both routes apply, the score blends them (55% direct, 45% through history) and the
Match stage marks the case with a green **via BIB-1204 · 82%** chip — but only when the
link actually changed the ranking, so the chip always means something.

## Migrating old qTest projects into the new tree

Consolidating several old projects into one tree means deciding, per case, where it now
belongs. The **Place in the new tree** panel lists every case whose path is not a node of
the tree and scores each node two ways:

- **like the cases there** — how much the case reads like the cases already placed at that
  node;
- **name overlap** — how much of the node's own distinctive vocabulary it uses. Words every
  node shares (*application, services, management*) weigh almost nothing; the words unique to one branch carry it. The old project label counts
  too, but capped, so a project named after an application nudges toward that
  application's node without outvoting what the case is actually about.

Each suggestion says which of the two produced it. Place a few by hand, and the rest sharpen
immediately — in testing, placing one case lifted its siblings from 1% to 33–44%. A bulk
action applies the top suggestion wherever it clears a threshold you set.

> Cold suggestions are weak when the cases are German and the tree is English, because
> vocabulary alone cannot bridge that. Place one case per branch first; the example route
> does not care about language.

## What the archive teaches the generator

Rather than guessing house style, the tool derives it:

- **Language** — the archive decides whether new cases are written in German or English.
  See below.
- **Naming pattern** — finds the longest leading run of segments that ≥60% of names share
  (`TC_`, `TF_`), a fixed trailing segment such as `…_Web_Regression` when ≥35% of names
  end with it, and whether a module slot is left in between. Three real conventions come
  out as `TC_{MODULE}_{TITLE}`, `TF_{MODULE}_{TITLE}_Web_Regression` and `[{MODULE}] {TITLE}`.
  Bracket modules (`[Modul] …`) and verb leads (`Verify …`) are recognised too. The result
  is an editable pattern with the tokens `{PREFIX} {MODULE} {REQ} {TYPE} {TITLE}`, and
  literal text is allowed anywhere in it.
- **Standard opening and closing steps** — any first or last step that appears in at least
  35% of archived cases (typically "An der App anmelden" / "Abmelden") is reused verbatim
  in every generated case, with the share it was found at shown in the UI.
- **Field values** — Type, Priority, Status and Module dropdowns are populated from the
  values your archive actually uses, so the qTest import does not fail on unknown options.
- **Your project's own qTest fields** — every column the tool does not recognise
  (`Version`, `Regressionstest`, `Test Owner`, `Testdauer`, `Testumgebung`, …) is carried through: each generated case is
  prefilled with the value your archive uses most, the fields are editable per draft, and
  they are written back out as their own export columns.
- **Precondition and module** — taken from the matched template case.

## Language of the generated text

Most archives are not bilingual by accident, so the language is read from the archive and
not guessed per run. On the **Generate** stage:

| Setting | Behaviour |
|---|---|
| **Auto** (default) | whatever language the archive is written in, shown next to the option |
| **Deutsch** | step phrasing, expected results, preconditions and the ISTQB technique names in German — `Prüfen: …`, `Der Wert wird mit einer Fehlermeldung abgewiesen.`, `Grenzwertanalyse`, `Äquivalenzklassenbildung – ungültige Klasse`, `Zustandsübergangstest` |
| **English** | the same scaffolding in English |

Two things deliberately do **not** follow this setting, because changing them would be a
translation rather than a choice:

- criterion text keeps the language of the Jira ticket it came from;
- the standard opening and closing steps are reused from the archive exactly as written.

So a German archive with an English ticket produces a case with German framing around
English criterion text — which is usually what you want while the two languages coexist.

## Converting cases you already have

The other direction through this tool, and a stage of its own because it is its own job.

**Cases can come from either side.** The knowledge base, if what you want to convert is
already there. Or a file dropped on the Convert stage itself, which lands in that stage
only — it never reaches the knowledge base, so a batch you want as a Tosca spec cannot
reshape the conventions the generator learned. If you later decide they should teach the
generator too, *Move into the knowledge base* does exactly that, with an undo.

Pick the destination there — Tosca, qTest, or both — and it sets the Export stage to match,
rather than naming a file it was not going to write.

**The copy is not the conversion.** Every field and every step is carried over word for
word, so in Review a converted case looks exactly like the case you started with — and the
card says so: *carried over whole, nothing on this card was written by the tool*. The
conversion is what sits underneath it: **the Tosca reading**.

### Why the reading is longer than the case

Tosca is three levels. A TestCase holds **TestSteps**; a TestStep is one **Module**, which
for SAP GUI means one screen; a **TestStepValue** is one control on that screen, with an
ActionMode of Input, Verify, Select, Buffer or WaitOn.

A manual step is none of those. It is a sentence for a person, and one sentence routinely
crosses a screen and fills four fields. So the reading has to **expand**, not translate:

| A manual SAP case says | Tosca needs |
|---|---|
| "Transaktion VA01 aufrufen" | a TestStep of its own with `OKCODE = /nVA01` — Tosca does not call transactions |
| "Auftragsart TA, Verkaufsorganisation 1000, Vertriebsweg 10 und Sparte 00 eingeben" | four Input lines on one screen, then the Enter |
| "…erfassen und sichern" | the fields, then Save as its own line |
| "Die Statusleiste nennt die vergebene Belegnummer" | a Verify **and** a Buffer — a person remembers the number, Tosca does not |
| "ein gültiger Kunde" | a value, or a TestCase-Design reference |

On the sample's `SAP-101` that is **4 written steps → 4 TestSteps and 14 TestStepValues**.

Screens come from the wording itself: the expected result of one step names the screen the
next step works on — *"Das Übersichtsbild wird angezeigt"* is where step four happens — and
that is the only screen boundary a manual case ever states. German names its screens in one
word, so `Einstiegsbild`, `Suchmaske` and `Startseite` come through whole, without the
article in front of them.

A step the whole archive repeats is not copied into every case. The 82% opening step
becomes `TSB_Bibliothekssystem_Anmelden`, referenced as a **reusable block** — which is
what the convention detection was finding all along without knowing it.

### The limit, stated plainly

**A runnable Tosca case cannot be generated from a manual one.** `Auftragsart` is the German
label a person reads; Tosca needs the **ModuleAttribute**, which only exists once somebody
scans that screen with Tosca's SAP engine. No amount of reading prose produces it.

What the export gives instead is a skeleton that is structurally right: the correct number
of TestSteps, split by screen, with the correct ActionModes, controls named as your wording
names them, and a **ModuleAttribute column left deliberately empty** for the automation
engineer to bind after the scan. The structuring is the tedious part, and that is the part
that is automated. Lines the sentence could not resolve are marked `<?>` rather than
invented.

The column names themselves stay provisional until a real Tosca export is available to
check them against; the reading below them does not depend on that.

## Carrying manual cases over to Tosca

A manual case that already exists in qTest does not need a requirement to be automated. On
the **Archive** stage, *Carry shown over to Review* (or the button on a single case) turns
archived cases into drafts, which then export like any other.

### Reading prose into TestStepValues

A manual step is a sentence; a Tosca TestStepValue is a triple of control, ActionMode and
value. The step text is read into those triples:

| In the step | Becomes |
|---|---|
| `Sortierung=Titel` | control `Sortierung`, **Input**, value `Titel` |
| `Aufrufen der Anwendung Katalog` | module `Katalog` — and it stays the module until a step names another |
| `eingeben`, `erfassen`, `pflegen` | **Input** |
| `auswählen`, `klicken`, `öffnen` | **Select** |
| `prüfen`, `wird angezeigt`, `enthält` | **Verify** |
| `warten` | **WaitOn** |
| `wird vergeben`, `notieren` | **Buffer** |
| the expected result | one **Verify** row per line |

Line breaks inside a step cell are preserved on import, because in a qTest export they are
the bullet list the tester wrote — one value each. Where a control cannot be read out, the
German article or the verb is skipped (`Die gesendete Nachricht…` → `Nachricht`, not `Die`;
`Kompletter Nachrichteninhalt` → `Nachrichteninhalt`). Every row keeps the sentence it came
from in a **Source sentence** column, so nothing has to be taken on trust.

Values the tool cannot derive are left empty rather than filled with invented Tosca syntax.

> **The column layout is provisional.** The reading above is settled; the column names are a
> best guess until a real Tosca export from the project is available to match.

## Test design techniques

Each acceptance criterion is classified, and the classification decides which cases are
forged:

| Signal in the criterion | Technique | Case produced |
|---|---|---|
| default | Equivalence Partitioning (valid class) | positive case |
| `invalid`, `Pflichtfeld`, `required`, `error`, `validation`, `darf nicht` | Equivalence Partitioning (invalid class) | negative case |
| numbers, ranges, `between … and`, `max`, `min`, `length`, `Zeichen`, `Grenze` | Boundary Value Analysis | min−1 / min / max / max+1 steps, with the real numbers from the text |
| `role`, `Berechtigung`, `permission`, `admin`, `only` | Decision Table | entitled vs. not-entitled role pair |
| `status`, `Zustand`, `from … to`, `Übergang`, `workflow` | State Transition | transition case |
| ≥ 2 criteria on one requirement | Use Case Testing | one end-to-end case chaining every criterion in order |

Gherkin criteria (`Given / When / Then`, `Angenommen / Wenn / Dann`) are split properly:
Given becomes the precondition, When the step action, Then the expected result. A
criterion that carries no trigger/outcome split becomes a `Prüfen: …` / `Check that …`
step and is flagged **needs wording**, so you can see at a glance which drafts still need
a human sentence.

## Import formats

### Archive

**`.xlsx` / `.xls` straight from qTest**, or CSV, semicolon-CSV or tab-separated with the
delimiter detected.

**One file is placed at one node of the module tree; each sheet inside it is a module.**
qTest writes one sheet per module, named after it (`MD-42 Katalog`), and the
rows inside carry no module column — so every sheet is imported and its name becomes the
module, with the leading module id stripped.

A qTest module tree is four to six levels deep and a sheet name only ever carries the
leaf, so the import is placed by its **full path**:

```
Anwendungen
  > Bibliothekssysteme
    > Katalogverwaltung
      > Katalogsuche
```

Paste the tree once — indented, as it appears in qTest, or one `A > B > C` path per line —
and every node becomes a suggestion on the import field, so a path is never typed twice.
Left empty, the file name is used.

The path is not decoration:

- the Archive stage shows a chip per node **at every level** with its case count, and
  filtering on a parent catches everything beneath it;
- renaming a node rewrites it wherever it appears in a path, and a branch can be dropped
  from the archive in one action;
- a requirement on the Match stage can be held to a node, which excludes every template
  outside that branch, so a transportation story never borrows a finance template;
- `{AREA}` (the leaf) is available in the naming pattern, and the **Module** column of the
  export carries the whole path, with a configurable separator since whether qTest splits
  it into sub-modules depends on the import settings.

Headers are matched case- and punctuation-insensitively against these aliases (not
exhaustive):

| Field | Recognised headers |
|---|---|
| Id | `Id`, `Test Case Id`, `Key`, `Nr`, `Nummer` |
| Name | `Name`, `Title`, `Summary`, `Testfall`, `Bezeichnung` |
| Description | `Description`, `Kurzbeschreibung`, `Beschreibung`, `Objective` |
| Precondition | `Precondition`, `Vorbedingung`, `Voraussetzung`, `Setup` |
| Step number | `Test Step #`, `Testschritt-Nr.`, `Schritt`, `Step` |
| Step action | `Test Step Description`, `Testschritt-Beschreibung`, `Schritte`, `Aktion` |
| Expected result | `Test Step Expected Result`, `Erwartetes Ergebnis`, `Sollergebnis` |
| Module | `Module`, `Modul`, `Folder`, `Component`, `Bereich` |
| Type / Priority / Status | `Testart`, `Priorität`, `Prio`, `Zustand`, … |
| Keywords | `Stichworte`, `Labels`, `Tags`, `Schlagworte` |

Matching runs alias by alias rather than column by column, so a project carrying both
`Type` and `Test type` maps the canonical one and leaves the other as a project field.
Everything else becomes a pass-through project field (up to 30 columns).

Two layouts are handled:

- **qTest style** — one row per step, the Id repeated and the name blank on continuation
  rows. Rows are grouped back into whole test cases. A step cell here may contain line
  breaks and its own bullet list; because the export has a step-number column, it stays
  one step.
- **Legacy Excel style** — all steps in one cell as a numbered list, with a single overall
  expected result, and no step-number column. The list is split into steps and the
  expected result lands on the last one.

**Test Run exports are recognised and flagged.** A run export is execution data: its `Id`
is the run (`TR-…`), its `Status` is the result (`Passed`), and it has no module or
precondition. It still imports — the step wording and naming convention are read from it —
but the Status column is deliberately not treated as a test-case status, and the page says
what is missing. Use *Test Design → Export Test Cases* for a real archive.

Where a column label appears twice — qTest writes `Test Case Id` for both the internal
number and the id you see (`TC-2134`) — the one that reads like an id wins and the other
becomes a project field.

### Requirements

- **Jira XML export** — the one on a single issue's *Export* menu, and the same shape for a
  whole filter. Worth knowing: its `<customfieldname>` names the acceptance-criteria field,
  so unlike the JSON path no field id has to be looked up. The escaped HTML inside
  `<description>` and the custom field is converted to text, with `<li>` becoming bullets
  and `<br>` a line break, which is exactly what the criterion parser wants. Exports
  carrying named HTML entities (`&auml;`) are not valid XML; those fall back to the lenient
  HTML parser instead of failing.
- **Jira CSV or Excel export** — `Issue key`, `Summary`, `Description`,
  `Custom field (Acceptance Criteria)`, `Components`, `Labels`, `Fix Version/s`,
  `Epic Link`. Jira's repeated `Labels` / `Components` / `Fix Version/s` columns are
  collected and joined.
- **Jira REST JSON** — the response of `/rest/api/3/search`. Atlassian Document Format
  descriptions are flattened to text. Add `&expand=names` to the query so the acceptance
  criteria custom field can be found by its label; otherwise type the field id (e.g.
  `customfield_10101`) into the field on the Requirements stage.

## Exporting into qTest

The export is one row per test step, which is what qTest's Excel/CSV import expects. By
default the column headers are **your archive's own labels**, so the mapping wizard shows
the names your project already uses:

```
Id;Name;Kurzbeschreibung;Vorbedingung;Modul;Type;Priorität;Status;Stichwort;
Testschritt-Nr.;Testschritt-Beschreibung;Erwartetes Ergebnis;
Version;Regressionstest;Test Owner;Testdauer;Testumgebung;
Anforderung;Abnahmekriterium;Testentwurfsverfahren;Abgeleitet aus (Archiv)
```

The first block is the qTest core, the second your project's own fields, the third the
optional traceability columns. A column your archive did not have falls back to the
language of the labels it *did* have, so an English export never grows a lone
`Vorbedingung`. German or English headers can be forced instead.

`Id` is left empty so qTest creates new test cases instead of updating existing ones.

In qTest: **Test Design → Import Test Cases → upload the file → map** `Name`,
`Description`, `Precondition`, `Test Step #`, `Test Step Description` and
`Test Step Expected Result`. The four traceability columns map to your own custom fields,
or switch them off before exporting.

Options: column headers (from the archive / Deutsch / English), delimiter (semicolon for
German Excel), UTF-8 BOM, repeat the name on every step row, approved-only, project fields
on/off, traceability columns on/off.

The second export is a **traceability matrix** — one row per requirement × criterion ×
test case, with requirements that have no coverage marked `— NO COVERAGE —`.

> The page is published as an Artifact, and that sandbox blocks downloads a page starts
> itself. Use **Copy** and paste into a file; **Save file** works when you open
> `index.html` from disk.

## Samples

| File | Shows |
|---|---|
| `samples/archive-de-qtest-export.csv` | the built-in sample: German qTest export with custom project fields and `…_Web_Regression` naming, ending in a weaker legacy block so the health bands have something to show |
| `samples/jira-requirements-de.csv` | the built-in sample: German tickets with bullets, Gherkin (`Angenommen/Wenn/Dann`) and duplicated `Labels` columns |
| `samples/archive-en-labels.csv` | a second project shape: English qTest labels around German content, bracket naming, no Precondition column, its own project fields |
| `samples/archive-qtest-export.csv` | the same shape in English |
| `samples/archive-legacy-excel.csv` | different German headers, comma-delimited, all steps in one cell |
| `samples/jira-requirements.csv` | English Jira CSV export |
| `samples/jira-issues.xml` | Jira XML export: two issues, HTML descriptions, criteria in a named custom field |
| `samples/jira-issues.json` | Jira Cloud REST response with an ADF description and a custom AC field |

The page loads a sample project on first open so you can see the whole pipeline working
before importing anything of your own. **Clear all** removes it.

## What it deliberately does not do

- It does not invent domain knowledge. A criterion that does not say what the expected
  result is produces a generic one, flagged **needs wording**. The drafts are a starting
  point for a test designer, not a replacement for one.
- It does not translate. Criterion text arrives in the language the ticket was written in
  and stays there; only the scaffolding the tool writes itself follows the language
  setting.
- It does not talk to Jira or qTest. Import and export are files you move yourself, which
  is also why no credentials are involved.
- It does not deduplicate against the archive. It tells you which existing case a draft was
  derived from and how close the match was; deciding whether to extend the old case instead
  of creating a new one stays with you.
