#!bin/bash


mkdir $BRANCH_DEST_NAME
cd $BRANCH_DEST_NAME
bzr init .
ruby $PATH_TO/bzr-super-replay2.rb $BRANCH_SRC_NAME 1 --module $MODULE_LIST

# Check diff

# Push LP_BRANCH_DEST_NAME

cd $BRANCH_SRC_NAME
bzr unbind
bzr rm $MODULE_LIST
bzr ci -m"[DEL] Remove module cause we move them to LP_BRANCH_DEST_NAME. Module list: MODULE_LIST"
bzr push $LP_BRANCH_SRC_NAME
bzr bind $LP_BRANCH_SRC_NAME

# Warning: This is really brute force and still has some bugs. Don't forget to make a diff after using it to verify that nothing has been lost.
