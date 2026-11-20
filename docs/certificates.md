# CERT SHARE v1: sharing a certificate on LinkedIn

Every course certificate can be shared the same way. It's all in the `CERT SHARE v1` block of
`index.html`, just above `COURSE v1`. It needs no server and nothing that costs money.

## What the learner sees

Under their certificate, a card called **Show it off on LinkedIn** has three numbered steps:

1. **Add it to your profile.** LinkedIn's free "Add to profile" form opens with the name
   ("Silver Key Certificate: … (Mapáchez Manor e-course)"), the issuer (KMC Creative Company, LLC),
   the month and year, the certificate ID and the **credential link** filled in. LinkedIn shows that
   link as the "Show credential" button.
2. **Add the skills.** LinkedIn's link can't fill in skills, so the skills are shown as chips with a
   **Copy skills** button to paste into the form's Skills box.
3. **Share a post.** **Share on LinkedIn** opens a new post with friendly text and the credential
   link. **Copy the post** and **Copy credential link** work anywhere else.

The certificate picture also has a small **QR code** (drawn with code, no library) that opens the
game, with "Earn yours at Mapáchez Manor" beside it, and the course line now reads "has completed
the Mapáchez Manor gamified e-course".

## The credential link

```
https://kmccreativecompany.github.io/Mapachez-Manor/?cert=SKC-CHK-1A2B-3C4D&n=Rosa+Quill&d=2026-11-20&k=R2JV
```

The details live in the link itself. `k` is a short check code made from the ID, name and date, so a
link that was edited or cut short shows a gentle "that link looks incomplete" note instead of a
certificate. Opening a good link shows the certificate, the skills practiced and an **Earn yours
free** button that starts the game. Viewing never changes the visitor's own saves.

This is honest about what it is: the page says certificates are made on the learner's own device
and that it shows the details carried in the link. It is a certificate of completion, not an
accreditation or license.

## Adding another course

A course registers once, after its own code:

```js
certRegister('hms',{                 // the middle part of its IDs: SKC-HMS-xxxx-xxxx
  course:()=>'HMS Basics',            // course name, in the player's language
  liName:()=>'Silver Key Certificate: HMS Basics (Mapáchez Manor e-course)',
  skills:()=>['Hotel Management Systems','Reservations'],
  draw:(canvas,d)=>drawMyCertificate(canvas,d)   // d = {id, name, date}
});
```

Then, on its certificate screen, call `certShareMount(host,{id,name,date})` for the share card,
and draw the QR with `drawQR(ctx,CERT_HOME,x,y,size)`. Credential links for that course work
automatically.

## Tests

`tests/test_cert_share.py` (run with `CHROMIUM_PATH=/opt/pw-browsers/chromium python tests/test_cert_share.py`).
If OpenCV is installed, the test also scans the QR code.

## Every certificate shares the same way

The three later courses (LUX, PHN, HSK) and the Master Certificate (MST) register too, so all five
certificates get the QR code, the credential link and the "Show it off on LinkedIn" card.
