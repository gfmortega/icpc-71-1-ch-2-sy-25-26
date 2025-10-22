# Knights and Knaves

Rampant industrialization can force us to confront the bleakness of an uncaring and increasingly materialistic world.  In such cases, many might find themselves joining a community which swears fealty not to physical objects but to grander principles that are larger than themselves... for better or for worse.

In this great city, there are two cults that dominate the land---the _Knights of Order_ and the _Knaves of Chaos_.  Each cult has but one simple rule.  Knights of Order **always tell the truth**.  Knaves of Chaos **always lie**.

I have here three friends of mine: `Alice`, `Bob`, and `Cindy`.  Each of them is either a Knight of Order, or a Knave of Chaos.  Your goal today is to determine the allegiance of each one (if possible).

Each of these people will say one statement, under oath.  Each of their statements will be one of ten possible kinds:
- `There is a knight among us.`
- `There is a knave among us.`
- `There are more knights than knaves.`
- `There are more knaves than knights.`
- `All of us are the same.`
- `Those other two are the same, and different from me.`
- `I am different from one of those two, but the same as the other one.`
- `Both of those two would say I am a knight.`
- `Both of those two would say I am a knave.`
- `If asked what I am, those two would give different answers.`

(where "those two" here refers to the two of my friends who are not the person currently speaking).

Beware paradoxes as well!

There will be $T$ independent test cases.

### Input Format

```
T
testcase1
testcase2
...
testcaseT
```
where each test case is described as follows:

```
Alice's statement
Bob's statement
Cindy's statement
------------------------------
```
where each statement is one of the ten described above, and this is followed by a line containing the `-` character $30$ times.

### Output Format

For each test case, output the answer.

First, consider that it may be possible for something fishy to occur.  That is, it is possible that if the scenario really were what I had described, then it should be impossible for my friends to have given those statements.  Then, there is only one liar... me!  Output a line containing the string `narrator: liar!` for this test case.

Otherwise, if it _is_ possible for people in the above scenario to have said those statements, then assume that everything I have said has been truthful.  For each of `Alice` and `Bob` and `Cindy`, output a line of the form `<name>: <status>`, where `status` is...

- `knight` if this person is surely a Knight of Order.
- `knave` if this person is surely a Knave of Chaos.
- `uncertain` if it is impossible to tell, using the given information.

Regardless, after every test case, also output a line containing `---------------` (the `-` character repeated $15$ times).


### Constraints

- $1 \leq T \leq 1000$

#### Sample Input 1

```
3
All of us are the same.
There is a knave among us.
I am different from one of those two, but the same as the other one.
------------------------------
Those other two are the same, and different from me.
There is a knight among us.
There are more knights than knaves.
------------------------------
Both my partners would say I am a knave.
There are more knaves than knights.
If asked what I am, those two would give different answers.
------------------------------
```

#### Sample Output 1

```
Alice: knave
Bob: knight
Cindy: knight
---------------
Alice: knave
Bob: uncertain
Cindy: knave
---------------
narrator: liar!
---------------
```


#### Explanation

In the first test case:
- Suppose that Alice is a knight.
  - Since her testimony is true, Bob and Cindy must be knights as well.
  - But if Bob is a knight, then his testimony of there being a knave among them must also be true.
  - But it's not true!  We said they were all knights!
  - This is a contradiction, therefore **Alice must be a knave.**
- Because Alice is a knave, Bob's testimony is true.  Therefore, **Bob must be a knight.**
- Since Alice and Bob have different allegiances, we conclude Cindy's testimony is true.  Therefore **Cindy must be a knight.**

In the second test case:
- Suppose that Bob is a knight.
  - There are no contradictions with his testimony---there is in fact a knight among them (him).
  - Suppose that Alice is a knight.
    - But if her testimony is true, then she and Bob should have different allegiances (which they do not).
    - This is a contradiction, therefore **Alice must be a knave.**
  - Suppose that Cindy is a knight.
    - But if Alice is a knave, then Alice's testimony should be false, and thus it should not be the case that both Bob and Cindy are knights.
    - This is a contradiction, therefore **Cindy must be a knave.**
  - Cindy is indeed a knave, because her statement of there being more knights than knaves is false, as $1 \not> 2$.
- Suppose instead that Bob is a knave.
  - Since his testimony is false, there must be no knights among them.
  - Therefore, **Alice and Cindy must also both be knaves**.
  - Alice is indeed a knave, because her testimony is false.  Bob and Cindy are of the same allegiance as her.
  - Cindy is indeed a knave, because her statement of there being more knights than knaves is false, as $0 \not> 3$.
- We cannot determine Bob's allegiance with certainty.  Despite that, logically, regardless of _his_ allegiance, we have deduced that Alice and Cindy are always both knaves.

In the third test case:
- Suppose that Alice is a knight.
  - She _isn't_ a knave, so for her testimony to be true (as a knight), we conclude that both Bob and Cindy would lie, therefore **Bob and Cindy must be knaves**.
  - But if Bob is a knave, then his testimony should be false.  But it _is_ the case that there are more knaves than knights.
  - This is a contradiction!
- Now, suppose that Alice is a knave.
  - She _is_ a knave, so for her testimony to be false (as a knave), we conclude that at least one of Bob or Cindy would lie, therefore at least one of those two is a knave.
  - This means there are at least two knaves among them---so Bob's testimony is true.
  - Therefore, **Bob must be a knight**, and **Cindy must be the knave.**
  - But is Cindy's testimony false?
    - Alice is a knave, so she would lie and say that Cindy is a knight.
    - Bob is a knight, so he would honestly say that Cindy is a knave.
    - Their answers differ, so Cindy's testimony is true.  But if she really were a knave, then her testimony should have been false!
  - This is a contradiction!

It is impossible for Alice to be a knight _or_ for her to be a knave.  Therefore the whole premise is false, and in this case, I (the narrator) was the one who lied to you!