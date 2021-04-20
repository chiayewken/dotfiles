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
set autoindent
set smartindent
set clipboard+=unnamedplus
colorscheme peachpuff

let mapleader=","
nnoremap ,, ,
nnoremap <leader>w :w<CR> :!ctags -R .<CR><CR>
nnoremap <leader>sn :NERDTreeToggle<CR>
nnoremap <leader>st :Tagbar<CR>
nnoremap <leader>ff :Files<CR>
nnoremap <leader>ft :Tags<CR>
nnoremap <leader>fl :Lines<CR>
nnoremap <leader>rf :ALEFix<CR>
nnoremap <leader>rn :ALERename
nnoremap <PageDown> <C-O>
nnoremap <PageUp> <C-I>
nnoremap gd :ALEGoToDefinition<CR>

let g:ale_fixers = {'python': ['black', 'isort'], 'markdown': ['prettier']}
let g:ale_linters = {'python': ['pyright'], 'bash': ['shellcheck']}
let g:ale_completion_enabled = 1
let g:sneak#label = 1
let g:tagbar_left = 1
let g:tagbar_foldlevel = 0
