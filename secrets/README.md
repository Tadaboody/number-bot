# Git-crypt
---
This directory includes secret files that were encrypted using [git-crypt](https://github.com/AGWA/git-crypt)

#### Unlocking git-crypt
to unlock the crypted files and use them you must create a gpg key using  
```
gpg --full-gen-key
```  
specifying your email as a user id. Later the user needs to be added using   

```
git-crypt add-gpg-user <USER_ID>
```  
run by someone who is already added. at which point running
```
git-crypt unlock
```
will unlock the repo (if you have a GPG key that was added)