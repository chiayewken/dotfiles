" https://github.com/junegunn/vim-plug/wiki/tips#automatic-installation
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
" Plug 'preservim/tagbar'
" Plug 'neovim/nvim-lspconfig'
" Plug 'airblade/vim-gitgutter'
" Plug 'davidhalter/jedi-vim'
call plug#end()

set shiftwidth=4
set autoindent
set smartindent
colorscheme peachpuff

" See :help last-position-jump
autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
    \ |   exe "normal! g`\""
    \ | endif

nnoremap <SPACE> <Nop>
let mapleader=" "
nnoremap <leader>q :q<CR>
nnoremap <leader>s :w<CR> :!ctags **/*.py *.py<CR><CR>
nnoremap <leader>ov :e $MYVIMRC<CR>
nnoremap <leader>ot :TagbarToggle<CR>
nnoremap <leader>rv :w<CR>:source $MYVIMRC<CR>
nnoremap <leader>ff :GFiles<CR>
nnoremap <leader>fb :Buffers<CR>
nnoremap <leader>fc :Command<CR>
nnoremap <leader>ft :Tags<CR>
nnoremap <leader>fl :Lines<CR>
nnoremap <leader>ae :ALENextWrap<CR>
nnoremap <leader>aE :ALEPreviousWrap<CR>
nnoremap <leader>af :ALEFindReferences<CR>
nnoremap <leader>ar :ALERename<CR>
nnoremap <leader>ah :ALEHover<CR>
nnoremap gd :ALEGoToDefinition<CR>

" autocmd FileType * TagbarOpen
let g:tagbar_position = 'left'
let g:tagbar_sort = 0
let g:tagbar_type_python = {'kinds' : ['c:classes', 'f:functions', 'm:members', '?:unknown']}
let g:ale_fixers = {'python': ['black', 'isort'], 'yaml': ['prettier'], 'markdown': ['prettier'], 'json': ['prettier'], 'sh': ['shfmt']}
let g:ale_linters = {'python': ['pyright', 'pylint'], 'sh': ['shellcheck']}
let g:ale_completion_enabled = 1
let g:ale_completion_autoimport = 1
let g:ale_fix_on_save = 1
let g:ale_python_pylint_options = '--disable=missing-function-docstring,missing-class-docstring,missing-module-docstring,too-few-public-methods,invalid-name,unspecified-encoding,import-error,no-name-in-module,line-too-long,too-many-return-statements,too-many-nested-blocks'
