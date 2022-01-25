#!/usr/bin/env bash
set -e

# Bash config
rm -rf ~/my_bashrc
ln -s "$PWD"/bashrc ~/my_bashrc
echo "source ~/my_bashrc" >> ~/.bashrc

# Tmux config
rm -rf ~/.tmux.conf
ln -s "$PWD"/tmux.conf ~/.tmux.conf

# Conda
if [[ ! -f Miniforge3-Linux-x86_64.sh ]]; then
	wget https://github.com/conda-forge/miniforge/releases/download/4.11.0-0/Miniforge3-Linux-x86_64.sh
fi
if [[ ! -d ~/miniforge3 ]]; then
	bash Miniforge3-Linux-x86_64.sh
fi

# Neovim
rm -rf ~/.config/nvim
mkdir ~/.config/nvim
ln -s "$PWD"/init.vim ~/.config/nvim/init.vim
if [[ ! -f nvim.appimage ]]; then
	wget https://github.com/neovim/neovim/releases/download/v0.6.1/nvim.appimage
fi
cp nvim.appimage ~
cd ~
chmod u+x ~/nvim.appimage
./nvim.appimage --appimage-extract
