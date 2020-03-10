# grocery app
Created this kivy app to help with my wife's weekly shop.

Requirements were simple enough:
  - store names of favourite dishes (crud - create, read, update, delete)
  - include main ingredients for each dish (more crud)
  - be able to use speech to text, including english and cantonese (what!)
  - option to select a dish for each day of the week
  - feature to auto-generate grocery list from the ingredients saved
  - option to customise grocery list
  - run it on her android
  - not look too shabby (I'm no ui expert but will do what I can)
  
Decided to write the code in python (3.6) using Kivy plus kv file. Just because I was getting the hang of python at the time.
Chose sqlite as "database" as it seemed the most straight forward.

Found a traditional chinese otf (SourceHanSerifTC-Medium.otf) from the web that worked a charm. Had to download SwiftKey Keyboard on android device as well since the chinese input on default samsung keyboard did not work for some reason.

To convert the code to android, I used buildozer, running on linux emulator (ubuntu). Word of caution, it takes around 30 mins to convert so make sure your code is in decent shape.

I used/doctored some images from the web (free ones) for the icons and graphics. 

One thing I learned on this journey is that in order to get from a to b, you will likely need to go via c, d and e!
But I realised how much I enjoyed coding and learning new technology, combating setbacks etc.

Note, I initially included options to backup the sqlite file to my google drive and restore it.
Code ran fine in windows but ran into permissioning errors when I tried it on android - apparently they limited the permissioning (after android 4 point something) and it is no longer easy to access application files. Closing some security loophole so I guess makes sense but does make it more difficult. Tried several ways to resolve (youtube) but still no joy. I can workaround the problem using adb on a rooted phone but was told by the wife not to root her phone! Works on my rooted device so thta's good I guess.
