call plug#begin('~/.vim/plugged')
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-fugitive'
Plug 'dense-analysis/ale'
Plug 'preservim/tagbar'
Plug 'justinmk/vim-sneak'
Plug 'sheerun/vim-polyglot'
Plug 'airblade/vim-gitgutter'
call plug#end()

set incsearch
set hlsearch
set ignorecase
set smartcase
set autoindent
set smartindent
colorscheme peachpuff

" See :help last-position-jump
autocmd BufReadPost *
	\ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
	\ |   exe "normal! g`\""
	\ | endif

let mapleader=","
nnoremap <leader>w :w<CR> :!ctags -R .<CR><CR>
nnoremap <leader>st :Tagbar<CR>
nnoremap <leader>ff :Files<CR>
nnoremap <leader>ft :Tags<CR>
nnoremap <leader>fl :Lines<CR>
nnoremap <leader>fe :ALENextWrap<CR>
nnoremap <leader>fv :e ~/.config/nvim/init.vim<CR>
nnoremap <leader>rf :ALEFix<CR>
nnoremap <leader>rn :ALERename<CR>
nnoremap <PageDown> <C-O>
nnoremap <PageUp> <C-I>
nnoremap gd :ALEGoToDefinition<CR>

let g:ale_fixers = {'python': ['black', 'isort', 'autoimport'], 'markdown': ['prettier'], 'sh': ['shfmt']}
let g:ale_linters = {'python': ['pyright'], 'sh': ['shellcheck']}
let g:ale_completion_enabled = 1
let g:ale_completion_autoimport = 1
let g:sneak#label = 1
let g:tagbar_left = 1
let g:tagbar_sort = 0
let g:tagbar_type_python = {'kinds': ['c:classes', 'f:functions', 'm:members']}
