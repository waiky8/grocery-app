# Grocery App
Another project to learn the basics of creating an android app.
This app was intented to help with the weekly shop.

Features:
  - store names of favourite dishes (crud - create, read, update, delete)
  - include main ingredients for each dish (more crud)
  - be able to use speech to text, including english and cantonese
  - enable dish to be selected for each day of the week
  - auto-generate grocery list from the ingredients of selected dishes
  - option to customise grocery list
  
Written in **python (3.6)** using **Kivy** plus **kv** file (for the layout) and **sqlite** as the "database" as it seemed the most straight forward.

Selected traditional **chinese otf** (SourceHanSerifTC-Medium.otf) and downloaded **SwiftKey Keyboard** on android device as the chinese input on the default samsung keyboard did not work for some reason.

**buildozer** was used to convert the code to run on android, running on **lubuntu** (**linux** emulator) from **oracle vn virtualbox** - buildozer only works on on linux if running on windows apparently. Warning - it takes around 30 mins to run conversion!

Note, sqlite file backup to google drive (plus restore) was initially included. Code ran fine in windows but encountered permissioning errors on android.
Discovered that the permissioning was limited (after android 4 I believe) and it is no longer possible to save/load external files easily. Closing some security loophole apparently. Eventually found a workaround using **adb** on a rooted phone, though phone needs to be rooted.

With a project like this, expect many unexpected issues - persevere!

Sample.<br>
![alt text](https://github.com/waiky8/grocery-app/blob/master/screenshots/screenshot2.png)
![alt text](https://github.com/waiky8/grocery-app/blob/master/screenshots/screenshot3.png)
![alt text](https://github.com/waiky8/grocery-app/blob/master/screenshots/screenshot4.png)
