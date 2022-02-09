" Auto-install plugins, see https://github.com/junegunn/vim-plug/wiki/tips#automatic-installation
let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin('~/.vim/plugged')
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-fugitive'
Plug 'dense-analysis/ale'
call plug#end()

set shiftwidth=4
set autoindent
set smartindent
colorscheme peachpuff

" Save previous position in files, see :help last-position-jump
autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
    \ |   exe "normal! g`\""
    \ | endif

nnoremap <SPACE> <Nop>
let mapleader=" "
nnoremap <leader><Esc> :q<CR>
nnoremap <leader><Tab> :e#<CR>
nnoremap <leader>b :Buffers<CR>
nnoremap <leader>c :Command<CR>
nnoremap <leader>e :ALENextWrap<CR>
nnoremap <leader>f :GFiles<CR>
nnoremap <leader>g :Git<CR>
nnoremap <leader>h :ALEHover<CR>
nnoremap <leader>l :Lines<CR>
nnoremap <leader>m :BLines<CR>
nnoremap <leader>r :ALERename<CR>
nnoremap <leader>s :w<CR> :!ctags **/*.py *.py<CR><CR>
nnoremap <leader>t :Tags<CR>
nnoremap <leader>u :BTags<CR>
nnoremap <leader>v :e $MYVIMRC<CR>
nnoremap <leader>w :ALEFindReferences<CR>
nnoremap <leader>z :w<CR> :source %<CR>
nnoremap gd :ALEGoToDefinition<CR>

let g:ale_fixers = {'python': ['black', 'isort'], 'yaml': ['prettier'], 'markdown': ['prettier'], 'json': ['prettier'], 'sh': ['shfmt']}
let g:ale_linters = {'python': ['pyright', 'pyflakes'], 'sh': ['shellcheck']}
let g:ale_completion_enabled = 1
let g:ale_completion_autoimport = 1
let g:ale_fix_on_save = 1
