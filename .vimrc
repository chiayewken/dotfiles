call plug#begin('~/.vim/plugged')
Plug 'preservim/nerdtree'
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-surround'
Plug 'dense-analysis/ale'
Plug 'preservim/tagbar'
Plug 'justinmk/vim-sneak'
Plug 'sheerun/vim-polyglot'
call plug#end()

set incsearch
set hlsearch
set ignorecase
set smartcase
colorscheme peachpuff
tnoremap <Esc> <C-\><C-n>

let mapleader=","
nnoremap ,, ,
nnoremap <leader>p :NERDTreeToggle<CR>
nnoremap <leader>f :Files<CR>
nnoremap <leader>w :w<CR> :!ctags -R .<CR><CR>
nnoremap <leader>b :Tagbar<CR>
nnoremap <leader>t :Tags<CR>
nnoremap <leader>x :ALEFix<CR>
nnoremap <PageDown> <C-O>
nnoremap <PageUp> <C-I>

let g:ale_fixers = {'python': ['black', 'isort']}
let g:ale_linters = {'python': ['pyright']}
let g:sneak#label = 1
let g:tagbar_left = 1
let g:tagbar_width = max([25, winwidth(0) / 5])
let g:tagbar_foldlevel = 0
