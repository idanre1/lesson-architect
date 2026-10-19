# Review: Your First Melody: Right Hand on a 61-Key Keyboard

## Structural check

Command, run from `examples/piano-first-melody/`:

```
python3 /home/idanre1/repos/lesson-architect/skills/lesson-architect/scripts/check_lesson.py lesson.md --blueprint lesson.blueprint.md
```

- **First draft:** 29 passed, 0 warnings, 0 failed (exit code 0).
- **After all revisions:** 29 passed, 0 warnings, 0 failed (exit code 0). The outcome counts in the blueprint and the lesson match (5 = 5).
- **Note:** a passing check shows only that the structure is present. The judgements below come from the continuity and correctness audits, which were done by reading the lesson and recomputing its facts.

## Continuity audit

The audit was a cold read of the whole lesson, done twice: once after drafting and once after the first round of fixes.

| Check | Verdict | Evidence / fix |
|---|---|---|
| Every learning outcome is taught and assessed | Pass | **O1** (find notes, C position): taught in §3 (black-key groups), WE1 (middle C) and §4 (C position). Assessed by E1 (guided) and E7 (transfer).<br>**O2** (posture, tension): taught in §2 and the warm-up; assessed by E4 (self-check list).<br>**O3** (beat and note lengths): taught in §5 and WE2; assessed by E2 (guided) and E6.<br>**O4** (play the melody steadily at ♩ = 60, 3× without stopping): taught in §6–§7 (table, WE3, joining bars, tempo ladder); assessed by E3 (guided, bars 1–4), E6 (the full criterion) and E7.<br>**O5** (short-loop fixing, self-judgement): taught in §6 and §7 (prediction and recording); assessed by E5 and E6. |
| Exercises require no untaught concepts | Pass, after fixes | **E6** asks for a recording and a count-in. "Count-in" was undefined, so it is now defined (R7). Recording on a phone was introduced in §7 before E6.<br>**E7** (G position) needs only the letter sequence from §3 and the finger numbers from §4. Its hint ties the new thumb key to a key the learner already used (R8). No staff notation, sharps or flats are needed anywhere. |
| Terminology and notation are introduced before use | Pass, after fixes | **Outcomes:** "middle C", "C position" and "quarter note" appear in the outcomes list before they are defined. A sentence now says they will be explained when first needed (R1).<br>**Forward reference:** the "steady" misconception referred to "the G in bar 4" before the melody table existed; it is now generic (R3).<br>**Defined before use:** "bar", "beat", "♩ = 60", the finger numbers and the "fingertip pad" (its wording is now unambiguous, R12). |
| Transitions preserve the learning thread | Pass, after fix | Each section opens by saying which of the three jobs (where, which finger, when) it adds. The transition into the practice section was generic and was rewritten (R9). The synthesis returns to the central question from the orientation. |
| Worked examples explain reasoning | Pass | **WE1** explains why the groups of two black keys locate C and why middle C is the 3rd C on a 61-key keyboard.<br>**WE2** derives each bar's beat total and says what lifting early sounds like (wording sharpened in R15).<br>**WE3** shows the loop (choose a spot, slow it down, repeat it correctly, then join it to the next bar) and says why each step is done. It now names the exact target note (R10). |
| Followable without filling missing conceptual steps | Pass, after fixes | **Fixed during the cold read:** <ul><li>a held note fades (R14), so beginners would otherwise re-press it;</li><li>a sustain pedal would blur the notes (R13);</li><li>the seat position for C position (R11);</li><li>why the answer to E1 is 6 Cs (R4);</li><li>the two different consequences of lifting early (R5).</li></ul>**Residual risk:** the lesson relies on a metronome, which the learner must find (built-in, app or website). The setup section explains this, but the lesson cannot help if none is available. |

## Correctness audit

Facts were checked by recomputing them in Python, by consulting primary or reference sources, and by comparing several independent sources for the melody.

| Check | Verdict | Evidence / fix |
|---|---|---|
| Claims, calculations, and code checked | Pass (one item hedged, one unsourced) | Summary of the rows below: melody, rhythm, fingering, transposition, keyboard layout and public-domain status verified; instrument-behaviour claim hedged; posture advice is general guidance without a cited source. No code. |
| 61-key layout: range, number of each note, middle C, centre key | Verified, with assumption | A standard 61-key keyboard runs C2–C7. Enumerating the keys in Python gives:<ul><li>6 Cs;</li><li>5 each of D, E, F, G, A and B;</li><li>middle C (C4) is the 3rd C from the left, key #25;</li><li>the centre key, #31, is F♯4, so middle C is a little left of centre, as the lesson says.</li></ul>Soloist ("How to Find Middle C on Any Keyboard") gives the same facts: 3rd C on 61 keys, and transpose/octave buttons change the sound but not which key is middle C. **Assumption:** the keyboard is C-to-C, which is stated in the lesson. |
| White-key names relative to black-key groups | Verified | Recomputed for every octave:<ul><li>C is just left of each group of two;</li><li>D is between the two;</li><li>E is just right of the group of two;</li><li>F is just left of each group of three;</li><li>G and A are between the keys of the group of three;</li><li>B is just right of the group of three.</li></ul>This matches the landmark table and the E1 solution. |
| Finger numbers and C position | Verified | Thumb = 1 to little finger = 5 is the standard convention (Wikipedia, "Fingering (music)"). In C position, right-hand fingers 1–5 cover C D E F G. Every finger in the melody table matches its note in C position: C→1, D→2, E→3, G→5. F (finger 4) is never used in the tune. |
| Rhythm values and tempo arithmetic | Verified | Quarter = 1 beat, half = 2 and whole = 4 beats in 4/4 (Wikipedia, "Note value"; "Tempo"). Every one of the 8 bars sums to 4 beats; the tune totals 32 beats. One play-through lasts 32 s at ♩ = 60 and 38.4 s at ♩ = 50. E6 (count-in, three run-throughs, 4 counted rest beats between them) totals 4 + 3×32 + 2×4 = 108 beats, so about 1 min 48 s at ♩ = 60. 60 bpm = one beat per second (Wikipedia, "Tempo"). |
| Melody notes (pitches) | Verified, from 3 sources | **Primary PD source:** the 1867 "Good-Night, Ladies" sheet music (Wikimedia Commons image, in B♭). I read its chorus as scale degrees: 3 2 1 2 3 3 3 · 2 2 2 3 5 5 · 3 2 1 2 3 3 3 · 2 2 3 2 1. In C that is E D C D E E E · D D D E G G · E D C D E E E · D D E D C.<br>**Cross-checks:** a modern C-major arrangement (Benchoom; viewed, not copied) gives the same notes. Skoove confirms the opening E D C D E E E.<br>**Version difference:** in "Mary", bar 6 has four Es rather than three (E E E E for "lamb, whose fleece was" / "Lit-tle lamb, its"). This comes from the extra syllable in Hale's words, and the Benchoom score has it too. The lesson uses the "Mary" version. |
| Melody rhythm and fingering | Verified | **Rhythm:** taken from the Benchoom score: quarters except the half notes at the ends of bars 2–4 and the whole note in bar 8. It is consistent with the 1867 chorus and with one syllable per note in Hale's words. A Python script checked that each row of the lesson's table has as many syllables as notes.<br>**Fingering:** 3212 · 333 · 222 · 355 · 3212 · 3333 · 2232 · 1, the same as Benchoom and Skoove (opening). |
| Transposition in E7 (G position) | Verified | Python moved every note up 7 semitones: B A G A · B B B · A A A · B D D · B A G A · B B B B · A A B A · G. This matches the E7 solution table, with the same finger numbers. The solution correctly says the tune sounds the same but higher. |
| Public-domain status | Verified | **Words:** a poem by Sarah Josepha Hale, published 1830 (Hale died 1879).<br>**Tune:** "Merrily We Roll Along", the chorus of "Goodnight, Ladies", published 1867 and attributed to E. P. Christy (died 1862). Sources: Wikipedia, "Mary Had a Little Lamb" and "Goodnight, Ladies".<br>**Our table:** written for this lesson; no arrangement is reproduced. "Hot Cross Buns" (suggested as a next step) is a traditional tune and is only named, not given. |
| Instrument-behaviour claims | Partly verified, hedged | **Pressing harder:** the claim that pressing harder does not make a held note longer and only changes loudness on touch-sensitive keys is hedged to "on almost every home keyboard", because some keyboards have aftertouch (R6).<br>**Fading:** the claim that a held piano-sound note fades is general knowledge and was not sourced.<br>**Pedal:** "A sustain pedal keeps notes sounding" is standard. |
| Posture and health advice | Not sourced | The advice (forearm roughly level, relaxed curved hand, stop if it hurts, short sessions) is mainstream beginner guidance. It is phrased cautiously and includes "stop if something hurts", but no source is cited. |
| Code and calculations | N/A / verified | The lesson contains no code. All the arithmetic above was recomputed. |

## Revisions made

These were made after the continuity and correctness audits; the checker was re-run after them.

- **R1:** added a sentence after the outcomes saying that new terms (middle C, C position, quarter note) are explained when first needed.
- **R2:** removed an unbounded "like slow footsteps" analogy from the warm-up. Footsteps are not evenly spaced in a way the learner could check.
- **R3:** removed a forward reference to "the G in bar 4" from the "steady" misconception, which appears before the melody table.
- **R4:** E1 solution:
  - simplified the explanation of why there are 6 Cs;
  - added the realistic "if you got 6" error for the count of Fs (the learner counted the Cs by mistake);
  - removed an implausible "10".
- **R5:** E2 solution: rewrote the unclear explanation of lifting early. If you keep counting, you hear a silent gap; if you don't, the next bar comes in too soon.
- **R6:** hedged the pressing-harder misconception for keyboards with aftertouch.
- **R7:** E6:
  - defined "count-in";
  - stated that the 4 counted rest beats between repetitions are not a stop.
- **R8:** E7: the hint now ties the G above middle C to the key that finger 5 used in C position. The solution wording now says exactly where C and D are in the next octave.
- **R9:** replaced the generic transition into the practice section with a specific one.
- **R10:** WE3 step 5 now names the target note: bar 5's first note, E, with finger 3.
- **R11:** the C-position paragraph now tells the learner to sit roughly opposite middle C.
- **R12:** "fingertip pad" was described as "just behind the nail", which is ambiguous. It is now "the fleshy underside of the last joint, near the tip". The analogy-boundary sentence that contradicted it was fixed to match.
- **R13:** settings: if a pedal is plugged in, keep your feet off it.
- **R14:** note lengths: a held note fades; keep holding it and do not re-press.
- **R15:** WE2 step 4: "if bar 2 felt shorter" became an observable check: "if your finger came up before you said '4'".
- **R16:** E6 pass criteria: "played with the finger in the table" cannot be judged from an audio recording. Finger checks now say to watch your hand or film it.
- **R17:** E1 hint: "count those [groups] instead of white keys" would give 5, not 6, because it misses the top C. The hint now says to use the groups to find each C and to check the rightmost key.
- **R18:** Sources: added the two modern arrangements used only for cross-checking (Benchoom, Skoove), so that the lesson's sources match the blueprint. Marked "Hot Cross Buns" as traditional.

## Not verified / limitations

- **Not tested with a learner:** the lesson has not been tried with a real beginner or at a real instrument. The pacing (sessions, tempo ladder ♩ = 50 → 60) is a reasoned estimate, not measured.
- **Pitches read by eye:** the 1867 pitches were read from a scanned image as scale degrees. The rhythm and the "Mary" bar 6 come from a modern arrangement plus the syllable count, not from an 1830s source with the "Mary" words set to music.
- **Keyboard models:** individual 61-key models were not checked. A few are not C-to-C, and the lesson tells the learner how to check. Transpose/octave settings vary by model, and the lesson gives only general advice.
- **Unsourced advice:** posture and tension advice is general guidance, not sourced or reviewed by a teacher or health professional.
- **Instrument behaviour:** the aftertouch hedge ("almost every") and the claim that a held note fades are general knowledge and are not tied to specific models.
- **Self-assessment:** the learner judges steadiness from a recording against a metronome. Small timing drift may be hard for a beginner to hear, so E6's criteria focus on large, audible errors (late starts, short holds, stops).

## Revisions after independent review

- Added a hint for E6 (independent exercise) after the skill began requiring hints on independent/transfer exercises.
- Added the summary correctness row above; the reviewer re-checked the melody table against the standard tune and the 1830/1867 dates against Wikipedia.
