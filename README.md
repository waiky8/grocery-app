# grocery app
Created this **kivy** app to help with my wife's weekly shop.

Requirements were simple enough:
  - store names of favourite dishes (crud - create, read, update, delete)
  - include main ingredients for each dish (more crud)
  - be able to use speech to text, including english and cantonese (what!)
  - option to select a dish for each day of the week
  - feature to auto-generate grocery list from the ingredients saved
  - option to customise grocery list
  - run it on her android
  
Decided to write the code in **python (3.6)** using **Kivy** plus **kv** file (for the layout).
Chose **sqlite** as "database" as it seemed the most straight forward.

Found a traditional **chinese otf** (SourceHanSerifTC-Medium.otf) from the web that worked like a charm. Had to download **SwiftKey Keyboard** on android device as well since the chinese input on default samsung keyboard did not work for some reason.

To convert the code to android, I used **buildozer**, running on **lubuntu** (**linux** emulator) from **oracle vn virtualbox** - buildozer only works on on linux if running on windows. Word of caution, it takes around 30 mins to convert so make sure your code is in decent shape first.

I used/doctored some images from the web (free ones) for the icons and graphics. 

One thing that I learned is that in order to get from a to b, you will likely need to go via c, d and e as well as overcome unforseen obstacles. A bucket-load of frustration but immensely satisfying in the end!

Note, I initially included options to backup the sqlite file to my google drive and restore it.
Code ran fine in windows but encountered permissioning errors when I tried it on android - apparently they limited the permissioning (after android 4 point something) and it is no longer easy to access application files. Closing some security loophole so makes sense I suppose. Tried several ways to resolve (youtube) but still no joy. I can workaround the problem using adb on a rooted phone but was told by the wife not to root her phone - ever! Works on my rooted device so at least I know it works.

Sample.<br>
![alt text](https://github.com/waiky8/grocery-app/blob/master/screenshots/screenshot2.png)
![alt text](https://github.com/waiky8/grocery-app/blob/master/screenshots/screenshot3.png)
![alt text](https://github.com/waiky8/grocery-app/blob/master/screenshots/screenshot4.png)
