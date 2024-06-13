from flask import Blueprint, render_template, session, redirect, requests, flash, url_for
from flask_login import current_user

import forms

from artigo_api import ArtigoApi
from utilizador_api import UtilizadorApi
from encomenda_api import EncomendaApi

blueprint = Blueprint('frontend',__name__)

@blueprint.context_processor
def cart_count():
    count=0
    encomenda = session.get('encomenda')
    if encomenda:
        for item in encomenda.get('linhas_encomenda'):
            count += item['quantidade']

    return {'total_artigos': count}

@blueprint.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        session['encomenda'] = EncomendaApi.get_encomenda_da_sessao
    try:
        artigos=ArtigoApi.get_artigos()
    except:
        artigos = {'result':[]}

    return render_template('index.html',artigos=artigos)

@blueprint.route('/registar', methods=['POST','GET'])
def registar():
    form = forms.RegistrationForm(request.form)
    if request.method =='POST':
        if form.validate_on_submit():
            nomeUtilizador = form.nomeutilizador.data

            if UtilizadorApi.get_utilizador_existente(nomeUtilizador):
                flash("Por favor escolha outro nome utilizador")
                return render_template('registar.html',form=form)
            else:
                utlizador = UtilizadorApi.criar_utilizador(form)
                if utlizador:
                    flash("Utilizador registado, faça login")
                    return redirect(url_for('frontend.index'))
        else:
            flash("Erros, codigos  10-21-987")
    return render_template('registar.html',form=form)


@blueprint.route('/login', methods=['POST','GET'])
def login():
    form = forms.LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            api_key=UtilizadorApi.login(form)
            if api_key:
                session['utilizador_api_key']=api_key
                utilizador = UtilizadorApi.get_utilizador()
                session['utilizador'] = utilizador['result']

                encomenda = EncomendaApi.get_encomenda()
                if encomenda.get('result'):
                    session['encomenda']=encomenda['result']
                flash('Bem vindo a loja S_$US')
                return redirect(url_for('frontend.index'))
            else:
                flash('Sem autorização')
        return render_template('login.html',form=form)

@blueprint.route('/logout',methods=['GET'])
def logout():
    session.clear()
    flash('Desligado')
    return redirect(url_for('frontend.index'))

@blueprint.route('/artigo/<cA>',methods=['GET','POST'])
def detalhes_artigos(cA):
    response = ArtigoApi.get_artigo(cA)
    artigo = response['result']

    form = forms.ItemForm(artigoId=artigo['id'])

    if request.method=='POST':
        if 'utilizador' not in session:
            flush("Por favor faça login")
            return redirect(url_for('frontend.login'))
        encomenda = EncomendaApi.adicionar_ao_carrinho(artigoId=artigo['id'],quantidade=1)
        session['encomenda']=encomenda['result']
        flash("Artigo adicionado ao carrinho")
    return render_template('artigoDetalhe.html',artigo=artigo, form=form)

@blueprint.route('/checkout', methods=['GET'])
def checkout():
    if 'utilizador' not in session:
        flash("Autentique-se")
        return redirect(url_for('frontend.login'))
    
    if 'encomenda' not in session:
        flash("Adicione uns artigos ao carrinho")
        redirect(url_for('frontend.index'))

    encomenda = EncomendaApi.get_encomenda()

    if len(encomenda['results']['linhas_encomenda']) == 0:
        flash("Adicione artigos primeiro")
        return redirect(url_for('frontend.index'))
    EncomendaApi.checkout()

    return redirect(url_for('frontend.volte_sempre'))


@blueprint.route('/volte_sempre', methods=['GET'])
def volte_sempre():
    if 'utilizador' not in session:
        flash("Autentique-se")
        return redirect(url_for('frontend.login'))
    
    if 'encomenda' not in session:
        flash("Adicione uns artigos ao carrinho")
        redirect(url_for('frontend.index'))

    session.pop('encomenda',None)
    flash("A encomenda foi processada")

    return render_template('obrigado.html')