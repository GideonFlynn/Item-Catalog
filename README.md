# Item catalog

###This is a catalog of items, each item is connected to a category.
_Category contains its own information and references items based on its id._

_An item contains its own information and has the possibility to reference a shop and a manufacturer._
#
####Each item can be connected to a shop and a manufacturer.


_A shop contains its own information_

_A manufacturer contains its own information_
#
The database could be represented like this:

Category > Item(Shop, Manufacturer)

Shop |

Manufacturer |


#Installation:
This code can run in a VirtualBox environment:
- Install VirtualBox
- Open a terminal(bash is nice)
- Run "vagrant init"
  ######This might take a while, go grab some water or do some exercises.
- Run "vagrant ssh"
  
  ######Congratulations! You are now able to access the vagrant folder inside your 'box'
    - Run "cd /vagrant"
  
  ######Now for the exiting part, running the app!
    - Run "python ItemCatalog.py"
  ######(You can write "python Item", then press tab
  ######The terminal will automatically try to find the name, which can save time)


TODO: Write usage instructions

#Contribution:
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


TODO: Write history


TODO: Write credits


TODO: Write license