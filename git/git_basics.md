# Chapter 1 : Git Intro

Git is a version control system
Git commands are funnily divided into 2 types : "Porcelain" and "Plumbing" [Toilet humor at its finest ig:) ]

# Chapter 2 : Git Repositories

git init ==> Create a empty git repository (ie. creates a .git hidden directory)

git status

git add <files here> ==> Stages file to index
git restore --staged <file name> ==> Unstages a file, but keeps in worktree.

git commit -m "Some message here"
git commit --amend ==> Lets us amend the last made commit (eg: git commit --amend -m "Modified Commit message" )

## Git log 

git log command display the commit history of the repo. Each commit is uniquely identifiable by a  SHA-1 hash		

git log --decorate=(short/full/no) => By default git log uses short decoration even without supplying the --decorate flag.

git log --oneline shows a more compact view of the logs

git --no-pager log ==> Run git log without the interactive pager mode		


# Chapter 3 : Git Internals
All the data about a git repository is stored inside the .git directory.
Git is "Just files all the way down".
Git is made up of "Objects" that are stored in .git/objects ; A commit is just a type of object.


If you try to cat .git/objects/0a/assdusdiosnvoisn , you will notice that it is compressed raw bytes.		
Instead git provides a plumbing utility called "cat-file".	

> git cat-file -p <hash>  

## Git Trees and Blobs
. tree - Git's way of storing a directory
. blob - Git's way of storing a file

> git cat-file -p 0f25fb2fb48ec194b575b5f018e7cf8488f4e664

When this command is run , it displays output as such

> tree 5b21d4f16a4b07a6cde5a3242187f6a5a68b060f     
> author Local User <localuser@skhbolla.github.io> 1758712992 +0000     
> committer Local User <localuser@skhbolla.github.io> 1758713682 +0000      

Notice that we can see:

. The tree object
. The author
. The committer
. The commit message
However, we cannot see the contents of the contents.md file itself! That's because the blob object stores it.

Now run the cat file with the hash of the tree. This returns the hash of the blob
git cat-file -p 5b21d4f16a4b07a6cde5a3242187f6a5a68b060f

> Output:
> 100644 blob ef7e93fc61a91deecaa551c4707e4c3049af42c9    contents.md

Now once again cat-file the blob		
git cat-file -p ef7e93fc61a91deecaa551c4707e4c3049af42c9

> Output:
> test content

**Notice that after the initial commit (which has no parents) , every commit's object will hold a extra field called parent. This will contain the hash of the parent commit**		

git cat-file -p 6efe83c0dcc50e541e924582eb57838dea03f2cc

> tree 37712fab0aa902b37e2197ebb71e4e1ba4f45f3d
> parent 0f25fb2fb48ec194b575b5f018e7cf8488f4e664
> author Local User <localuser@skhbolla.github.io> 1758717771 +0000
> committer Local User <localuser@skhbolla.github.io> 1758717771 +0000


**Git stores an entire snapshot of files on a per-commit level. This was a surprise to me! I always assumed each commit only stored the changes made in that commit.**

While it's true that Git stores entire snapshots, it does have some performance optimizations so that your .git directory doesn't get too unbearably large.		

. Git compresses and packs files to store them more efficiently.
. Git deduplicates files that are the same across different commits. If a file doesn't change between commits, Git will only store it once.


# Chapter 4 : Git Config - In Depth Guide

git config ==> responsible for managing the configuration files

git configurations can be made at 4 different locations. 
They are (in order of Precedence):
. Worktree level (inside .git/config.worktree file) 
. Local level (inside the repo's .git/config file)
. Global level (inside the user's home directory ~/.gitconfig)
13.233.254.133. System level (inside /etc/gitconfig file)

**Remember that if same key is present in more than 1 config file , the higher precedence config overrides the rest**

Note that , Git config keys are case-insensitive, For example , defaultBranch and defaultbranch work the same. Git just prefers lowercase when displaying them.

git config --local --list
git config --local --add user.name "Local User"
git config --global --add user.name "Global User"
git config --local --get user.name
git config --local --unset user.name
git config --local --remove-section user ==> Removes the entire user section


To remove a value from config , use --unset flag; But to remove an entire section use --remove-section flag.

**Typically, in a key/value store, like a Python dictionary, you aren't allowed to have duplicate keys. Strangely enough, Git doesn't care.**

So , if you add multiple values for the same key in the same config, then the latest added (bottom of file is considered)		

Since , --unset flag removes only 1 instance (latest) of a key , we can use --unset-all to remove all instances.		


# Chapter 5 : Branching

A Git branch allows you to keep track of different changes separately.

**Under the Hood**		

A **branch is just a named pointer to a specific commit**. When you create a branch, you are creating a new pointer to a specific commit. The commit that the branch points to is called the tip of the branch.

To check which branch we are currently on, use:
> git branch 

To rename a branch , use:
> git branch -m oldname newname

To create a new branch, you can use one of the two methods:
> git branch new_branch_name 
This creates a new branch. The thing is, I rarely use this command because usually I want to create a branch and switch to it immediately. So I use this command instead:

> git switch -c new_branch_name
The switch command alows to switch brances , -c flag creates branch if it doesnot exist.		

**Note that an old of just switching between branches is "git checkout Branch_name"**

**When you create a new branch , it uses the current commit you are on as the branch base**

For example , after we create a new branch called "add_classics" and run the git log command, the output shows the head still pointing to main ; but more importantly the **commit will also show that add_classics references this commit**

> commit ac1b688815cb6313cda4f4fbc02a0dc729002987 (HEAD -> main, add_classics)

Now switch to add_classics using git switch. The head now points to add_classics

> commit ac1b688815cb6313cda4f4fbc02a0dc729002987 (HEAD -> add_classics, main)

**Clarification : In git log's output , After a commit's SHA, Git is showing you all the references that point to that commit. In this case ,**

1. "HEAD -> add_classics" means that HEAD is pointing to add_classics , and add_classics inturn points to the commit		

2. "main" means that the branch main is also pointing to this commit		


------

# Chapter 6 : Git Merge

Let's say you're in a state where you have two branches, each with their own unique commits:		

If you merge some_new_branch into main (with both main and some_new_branch having their own commits), Git combines both branches by creating a new commit that has both histories as parents.

```
Before merge:

A - B - C    main		
   \		
    D - E    some_new_branch		


After merge: 

A - B - C - F    main		
   \     /		
    D - E        some_new_branch		


```

## Merge Commit
A merge commit is the result of merging two branches together.

In the above example , when we merge the some_new_branch to main , it created a merge commit. The exact process is as follows:

1. Find the "**merge base**" commit, also called the "best common ancestor" of the two branches. In this case , A 
2. Replay the changes from main, starting from the best common ancestor, into a new commit.
3. Replay the changes from vimchadsonly onto main, starting from the best common ancestor.
4. Records the result as a new commit, in our case, F.
5. **F is special because it has two parents, C and E.**
 
## Fast Forward Merge
The simplest type of merge is a fast-forward-merge.


Let's say we start with this:

```

      C     delete_vscode
     /
A - B       main

```
And we run this while on main:

git merge delete_vscode

Because delete_vscode has all the commits that main has, Git automatically does a fast-forward merge. It just moves the pointer of the "base" branch to the tip of the "feature" branch:

```

            delete_vscode
A - B - C   main

```

Notice that with a fast-forward merge, no merge commit is created.

**In a fast-forward merge, Git doesnâ€™t create a new commit at all. It simply moves the branch pointer forward to the target commit. Since no new commit is made, thereâ€™s no question of multiple parents â€” the history remains a straight line**

-------

# Chapter 7 : Rebase

Both rebase and merge can be used to integrate changes from one branch into another. But each has its own distinct use case.

Say we have this commit history:

A - B - C    main
   \
    D - E    feature_branch

We're working on feature_branch, and want to bring in the changes our team added to main so we're not working with a stale branch. We could merge main into feature_branch, but that would create an additional merge commit. **Rebase avoids a merge commit by replaying the commits from feature_branch on top of main**. After a rebase, the history will look like this:

A - B - C         main
         \
          D - E   feature_branch

## How rebase works internally

To use rebase to bring changes from main onto a current branch (let's pretend we're on one called jdsl), we would run this while on the jdsl branch:

> git rebase main

This will do the following:

1. Identify the latest commit from main and use it as the temporary new base for the rebase process
2. Replay each commit from jdsl one at a time onto this temporary location
3. Update the jdsl branch to point to the last replayed commit in the temporary location, making this the new permanent jdsl.
4. The rebase does not affect the main branch; jdsl now includes all changes from main.

**Remember that when we rebase a branch , the commits associated with that branch will get new SHAs because we are changing the parent commit**

## When to rebase

git rebase and git merge are different tools.

An advantage of merge is that it preserves the true history of the project. It shows when branches were merged and where. One disadvantage is that it can create a lot of merge commits, which can make the history harder to read and understand.

A linear history is generally easier to read, understand, and work with. Some teams enforce the usage of one or the other on their main branch, but generally speaking, you'll be able to do whatever you want with your own branches.

## Never rebase a public branch

You should never rebase a public branch (like main) onto anything else. Other developers have it checked out, and if you change its history, you'll cause a lot of problems for them.

However, with your own branch, you can rebase onto other branches (including a public branch like main) as much as you want.

## Understanding git rebase Beyond “branch onto branch”

Got it — let’s make it blog-post style, still in points but more structured and explanatory.

---

### Understanding `git rebase` Beyond “branch onto branch”

* **Rebase has multiple faces**
  Most people think of `git rebase` only as a way to “move a branch onto another branch” (e.g., putting your feature branch on top of `main`). That’s true, but it’s only half the story. Rebase can also be used locally to rewrite your own branch’s history — reordering commits, squashing them together, or editing commit messages.

* **Interactive rebase (`-i`) is the key**
  Running `git rebase -i HEAD~N` tells Git:

  > “Take the last N commits of my current branch and rebuild them one by one, letting me edit their order or content.”

* **Replay onto the same parent**
  In this form, Git doesn’t move you onto another branch. Instead, it replays your commits on top of their existing parent commit. Example:

  ```bash
  git checkout feature
  git rebase -i HEAD~3
  ```

  If `feature` had commits `D → E → F` based on `B`, Git will let you rewrite those commits, but your branch will still diverge from `main` at `B`.

* **When to use this**

  * To squash multiple small commits into a single clean one.
  * To reorder commits so history reads more logically.
  * To edit an old commit message or even change the contents of a commit.
  * To drop unnecessary commits entirely.

* **Contrast with rebasing onto another branch**

  * `git rebase main`: moves your branch so its commits replay on top of `main`’s latest commit.
  * `git rebase -i HEAD~3`: stays within your current branch, just rewrites your last 3 commits.

* **Takeaway**
  Think of `git rebase` in two categories:

  1. **Branch rebase** → move your branch to start from another branch.
  2. **History cleanup (interactive rebase)** → rewrite, reorder, squash, or drop commits within your current branch.


-----

# Chapter 8 : Reset

One of the major benefits of using Git is the ability to undo changes. There are a lot of different ways to do this, but first, we'll start by going back in the commit history without discarding changes.

## Git reset soft

The git reset command can be used to undo the last commit(s) or any changes in the index (staged but not committed changes) and the worktree (unstaged and not committed changes).

> git reset --soft COMMITHASH

The --soft option is useful if you just want to **go back to a previous commit, but keep all of your changes**. Committed changes will be uncommitted and staged, while uncommitted changes will remain staged or unstaged as before.

## Git reset Hard

The git reset --hard command resets your current branch and working directory to a specific commit (by default, the last commit). 	

Specifically, it does the following:

. Committed changes â€” Any commits after the target commit are discarded.
. Staged changes (index) â€” Files staged but not committed are reset.
. Working directory â€” All tracked files in the working tree are reverted to match the target commit.

**Important:**

**Untracked files are not affected.**

**If a file is untracked, Git has never staged or committed it, so git reset --hard does not touch it.**

In short: git reset --hard only resets files that Git is already tracking; it does not delete untracked files.

> git reset --hard <commithash>

==Reset --hard is a very dangerous command because changes will be lost forever if not careful. Use safer alternatives , and use --hard only when absolutely necessary==

----

# Chapter 9 : Git Remote


A remote in Git is simply a reference to another repository, usually hosted on a platform like GitHub, GitLab, or Bitbucket (But can even be another repo on the same device too). It allows the repository on your machine to communicate with the external one, so you can fetch changes others have made, push your own commits, and keep multiple copies of a project in sync. When you add a remote, Git records it under a name and associates it with a URL. Fetching from a remote brings in all of its branches and commits, storing them as remote-tracking branches (like origin/main) in your local repo.			

The standard convention is that when you're treating the remote as the "authoritative source of truth" (such as GitHub) you would name it the "origin".			

To add a remote to your repo , use:

> git remote add <name> <uri>

## Git Fetch

Adding a remote to our Git repo does not mean that we automagically have all the contents of the remote. First, we need to fetch the contents.		

> git fetch 

This downloads copies of all the contents of the .git/objects directory (and other bookkeeping information) from the remote repository into your current one.


**Just because we fetched all of the metadata from the remote webflyx repo doesn't mean we have all of the files.**


TIP: You can use "git log remote/branch" to view the commit history of a remote branch.

## Merge

Just as we merged branches within a single local repo, we can also merge branches between local and remote repos.

> git merge remote/branch

For example, if you wanted to merge the "some_remote_branch" branch of the remote origin into your local main branch, you would run this **inside the local repo while on the main branch**:

> git merge origin/some_remote_branch

### Useful TIP:

> git branch -r 

Shows all the remote-tracking branches that your local git repo knows about.

------

# Chapter 10 : GitHub

GitHub is the most popular website for Git repositories (projects) online. That is, for hosting "remotes" on a central website. GitHub serves several purposes:

. As a backup of all your code on the cloud in case something happens to your computer
. As a central place to share your code and collaborate on it with others
. As a public portfolio for your coding projects

## Git push 

The git push command pushes (sends) local changes to any "remote" - in our case, GitHub. For example, to push our local main branch's commits to the remote origin's main branch we would run:

> git push origin main

**You can also push a local branch to a remote with a different name:**

> git push origin <localbranch>:<remotebranch>

**You can also delete a remote branch by pushing an empty branch to it:**

> git push origin :<remotebranch>


## Git Pull

> git pull [<remote> <branch>]

The [...] syntax means that the bracketed remote and branch are optional. If you execute git pull without anything specified it will pull your current branch from the remote repo. 

## Typical team workflow in git

. Update my local main branch with "git pull origin main"
. Checkout a new branch for the changes I want to make with "git switch -c <branchname>"
. Make changes to files
. git add .
. git commit -m "a message describing the changes"
. git push origin <branchname> (I push to the new branch name, not main)
. Open a pull request on GitHub to merge my changes into main
. Ask a team member to review my pull request
. Once approved, click the "Merge" button on GitHub to merge my changes into main
. Delete my feature branch, and repeat with a new branch for the next set of changes


### Important

Even after you merge a feature branch into main and delete it on the remote (origin), the branch and its commits can still appear locally because Git keeps your local references independent of the remote. Your local repository maintains pointers to remote branches (like origin/feature) and the commits themselves, so the history remains visible in "git log remote/feature" until those references are updated.		

Pruning is needed to clean up these stale references. Running "git fetch --prune remote" removes local pointers to branches that no longer exist on the remote, keeping your repository tidy and ensuring that git branch -r accurately reflects the current state of the remote. This doesnâ€™t delete any commits that are already merged; it only removes the outdated branch references.


-------

# Chapter 11 : GitIgnore

