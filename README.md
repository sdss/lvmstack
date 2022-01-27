# lvm superproject

## clone with all lvm modules

    git clone --recurse-submodules -j8  --remote-submodules https://github.com/wasndas/lvm.git
    
For already cloned repos, or older Git versions, use:

    git clone https://github.com/wasndas/lvm.git
    cd bar
    git submodule update --init --recursive
    
## update 

    git submodule update --remote
    

