alias tm="TERM=xterm-256color tmux"
alias p="python -m pdb -c continue"
alias v="~/squashfs-root/usr/bin/nvim"
alias vpy="~/squashfs-root/usr/bin/nvim *.py */*.py */*/*.py"
alias gs="git status"
alias gd="git diff"
alias ns="nvidia-smi"
alias ca="conda deactivate && conda deactivate && conda activate"
alias sb="source ~/.bashrc"
alias oss="~/ossutil64"

cu() {
	export CUDA_VISIBLE_DEVICES="$1"
	echo CUDA="$CUDA_VISIBLE_DEVICES"
}

cr() {
	name=$1
	conda deactivate
	conda deactivate
	conda remove -n "$name" --all -y
	conda env create --file environment.yml
	conda activate "$name"
}
