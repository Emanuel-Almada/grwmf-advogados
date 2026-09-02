# -*- coding: utf-8 -*-
"""
Conteúdo do site GR & WMF Advogados.

Toda a copy do site vive aqui. Regra editorial (Provimento 205/2021 da OAB):
sem preço, sem promessa de resultado, sem caso de êxito, sem depoimento de
cliente, sem linguagem mercantil ("o melhor", "líder", "garantimos").
A autoridade se demonstra por qualificação, clareza e conteúdo útil.
"""

SITE = {
    "nome": "GR & WMF Advogados",
    "dominio": "https://www.grewmfadvogados.com",
    "cidade": "Belo Horizonte",
    "bairro": "Barreiro",
    "uf": "MG",
    "endereco": "Rua Flávio Marques Lisboa, 511 — 2º andar, Barreiro",
    "cep": "30640-050",
    "email": "contato@grewmfadvogados.com",
    "horario": "Segunda a sexta, das 9h às 18h",
    "horario_schema": "Mo,Tu,We,Th,Fr 09:00-18:00",
    "geo": {"lat": "-19.9737", "lng": "-44.0247"},
    "whatsapp": "5531984565235",          # E.164 — apenas dígitos
    "whatsapp_2": "5531984732625",
    "tel_exibicao": "(31) 98456-5235",
    "tel_exibicao_2": "(31) 98473-2625",
    "fundacao": "2026",
}

# ---------------------------------------------------------------- advogados

ADVOGADOS = [
    {
        "slug": "gabriella-reis-antunes-ferreira",
        "nome": "Gabriella Reis Antunes Ferreira",
        "trato": "Dra.",
        "oab": "OAB/MG 224.424",
        "cargo": "Sócia — Família, Sucessões, Imobiliário e Condominial",
        "whatsapp": SITE["whatsapp"],
        "tel": SITE["tel_exibicao"],
        "resumo": "Atua em divórcios, inventários, guarda e questões imobiliárias, "
                  "com formação em conciliação e mediação — o que permite resolver "
                  "boa parte dos casos sem litígio.",
        "formacao": [
            "Pós-graduada em Direito de Família e Sucessões",
            "Pós-graduanda em Direito Imobiliário",
            "Formação em Conciliação e Mediação de Conflitos",
        ],
        "areas": ["familia-e-sucessoes", "direito-imobiliario", "direito-condominial"],
        "bio": [
            "Gabriella atua nas áreas de Direito de Família e Sucessões, Direito "
            "Imobiliário e Direito Condominial, conduzindo demandas judiciais e "
            "extrajudiciais voltadas à proteção do patrimônio, à organização "
            "familiar e à solução de conflitos com segurança jurídica.",
            "É pós-graduada em Direito de Família e Sucessões e pós-graduanda em "
            "Direito Imobiliário. A formação em Conciliação e Mediação de Conflitos "
            "orienta boa parte da sua prática: sempre que o caso permite, a via "
            "consensual é buscada primeiro, porque costuma ser mais rápida e menos "
            "desgastante para quem está envolvido.",
            "O atendimento é individualizado. Cada caso de família carrega uma "
            "história, e a orientação jurídica só é útil quando parte do que a "
            "pessoa realmente está vivendo.",
        ],
        "foto": "/assets/img/advogada-gabriella.jpg",
        "iniciais": "GR",
    },
    {
        "slug": "welberth-martins-ferreira",
        "nome": "Welberth Martins Ferreira",
        "trato": "Dr.",
        "oab": "OAB/MG 183.884",
        "cargo": "Sócio — Trabalhista, Empresarial e Contratual",
        "whatsapp": SITE["whatsapp_2"],
        "tel": SITE["tel_exibicao_2"],
        "resumo": "Atua em causas trabalhistas e na assessoria jurídica de empresas, "
                  "tanto na defesa de empregadores quanto na de trabalhadores, com "
                  "foco em prevenir o litígio antes que ele exista.",
        "formacao": [
            "Atuação em Direito do Trabalho e Direito Empresarial",
            "Experiência em contencioso trabalhista e gestão de passivos",
            "Consultoria preventiva para empresas e profissionais",
        ],
        "areas": ["direito-trabalhista", "direito-empresarial", "direito-contratual"],
        "bio": [
            "Welberth atua em Direito Trabalhista e Direito Empresarial, conduzindo "
            "demandas judiciais e extrajudiciais voltadas à defesa de direitos, à "
            "redução de riscos jurídicos e à estruturação segura das relações de "
            "trabalho e das atividades empresariais.",
            "Presta assessoria a empresas e profissionais em litígios trabalhistas, "
            "consultoria preventiva, gestão de passivos e organização jurídica do "
            "negócio. Também atua na defesa de trabalhadores quando há violação de "
            "direitos.",
            "A prática combina rigor técnico e visão estratégica: entender o "
            "objetivo do cliente antes de escolher o caminho processual costuma "
            "evitar disputas longas e caras.",
        ],
        "foto": "/assets/img/advogado-welberth.jpg",
        "iniciais": "WM",
    },
]

# ---------------------------------------------------------------- áreas

AREAS = [
    {
        "slug": "familia-e-sucessoes",
        "nome": "Família e Sucessões",
        "icone": "familia",
        "dor": "Divórcio, inventário, guarda ou pensão — decisões que envolvem "
               "patrimônio e pessoas ao mesmo tempo.",
        "resumo": "Conduzimos separações, inventários e questões de guarda buscando "
                  "primeiro o acordo. Quando não é possível, entramos com a ação.",
        "meta_title": "Advogado de Família e Inventário em BH",
        "meta_desc": "Divórcio, inventário, guarda e pensão em Belo Horizonte. "
                     "Atendimento com prioridade para acordo e mediação. "
                     "Fale com a GR & WMF Advogados.",
        "h1": "Direito de Família e Sucessões",
        "lead": "Quando a vida muda — uma separação, uma perda, uma discussão sobre "
                "guarda — o problema jurídico vem junto com o problema humano. "
                "Nossa atuação começa entendendo os dois.",
        "quando": [
            "Você decidiu se separar e quer entender como fica a partilha e a guarda",
            "Um familiar faleceu e o inventário ainda não foi aberto ou está parado",
            "A pensão alimentícia não está sendo paga",
            "A guarda ou o regime de visitas precisa ser revisto",
            "É preciso interditar ou assumir a curatela de um familiar",
        ],
        "servicos": [
            ("Divórcio consensual e litigioso", "Judicial ou em cartório, conforme o caso permitir."),
            ("Partilha de bens", "Definição do que é comum, do que é particular e de como dividir."),
            ("Inventário e partilha", "Extrajudicial em cartório quando há acordo; judicial quando não há."),
            ("Pensão alimentícia", "Fixação, revisão e exoneração."),
            ("Cobrança de pensão", "Cumprimento de sentença, incluindo os meios de cobrança previstos em lei."),
            ("Guarda e convivência", "Definição, revisão e regulamentação do convívio com os filhos."),
            ("Curatela e interdição", "Proteção jurídica de quem não pode praticar atos da vida civil."),
            ("União estável", "Reconhecimento, dissolução e contratos de convivência."),
        ],
        "faq": [
            ("Quanto tempo demora um inventário?",
             "Depende do caminho. Havendo acordo entre os herdeiros e todos sendo "
             "maiores e capazes, o inventário pode ser feito em cartório e costuma "
             "levar semanas. Havendo disputa, testamento ou herdeiro menor, ele "
             "corre na Justiça e o prazo é maior. Na primeira conversa conseguimos "
             "dizer em qual dos dois cenários o seu caso está."),
            ("Dá para se divorciar sem ir à Justiça?",
             "Sim. Se o casal está de acordo e não há filhos menores ou incapazes, "
             "o divórcio pode ser feito em cartório, com assistência de advogado. "
             "É mais rápido e menos custoso do que o processo judicial."),
            ("Existe prazo para abrir o inventário?",
             "Sim. A legislação prevê a abertura em até 60 dias do falecimento, e a "
             "perda desse prazo pode gerar multa sobre o imposto estadual (ITCMD). "
             "Se o prazo já passou, ainda é possível regularizar — quanto antes, "
             "menor o impacto."),
            ("Precisa de advogado para acordo de guarda?",
             "Para que o acordo tenha força de decisão judicial, sim: ele precisa "
             "ser homologado, e isso é feito com advogado. Um acordo apenas "
             "combinado entre as partes não protege ninguém se for descumprido."),
        ],
    },
    {
        "slug": "direito-imobiliario",
        "nome": "Direito Imobiliário",
        "icone": "imovel",
        "dor": "Comprar, vender ou regularizar um imóvel sem descobrir o problema "
               "depois da assinatura.",
        "resumo": "Análise de documentação, contratos, escritura, registro, "
                  "usucapião e regularização de matrícula.",
        "meta_title": "Advogado Imobiliário em Belo Horizonte",
        "meta_desc": "Contratos imobiliários, usucapião, regularização de matrícula "
                     "e análise de documentação de imóvel em Belo Horizonte. "
                     "GR & WMF Advogados.",
        "h1": "Direito Imobiliário",
        "lead": "Imóvel é o maior patrimônio da maioria das famílias. A diferença "
                "entre uma compra tranquila e um problema de anos costuma estar na "
                "documentação que ninguém leu antes de assinar.",
        "quando": [
            "Você vai comprar um imóvel e quer conferir a documentação antes de pagar",
            "A obra atrasou e você quer saber se pode rescindir o contrato",
            "O imóvel está ocupado há anos mas não está no seu nome",
            "A matrícula tem pendências, averbações faltando ou construção não registrada",
            "Um imóvel de herança precisa ser vendido ou dividido entre herdeiros",
        ],
        "servicos": [
            ("Contratos imobiliários", "Elaboração e revisão de compra e venda, permuta e locação."),
            ("Análise de documentação", "Verificação de matrícula, certidões e riscos antes da negociação."),
            ("Escritura e registro", "Acompanhamento no cartório até o imóvel estar no seu nome."),
            ("Usucapião", "Judicial ou extrajudicial, conforme a situação do imóvel."),
            ("Regularização de matrícula", "Averbação de construção, retificação de área e pendências."),
            ("Atraso na entrega de obra", "Rescisão, devolução de valores e indenização."),
            ("Imóvel em condomínio de herdeiros", "Solução consensual ou judicial da divisão."),
            ("Distratos e rescisões", "Análise das cláusulas e negociação das condições de saída."),
        ],
        "faq": [
            ("O que precisa ser checado antes de comprar um imóvel?",
             "No mínimo: matrícula atualizada, certidões do imóvel e do vendedor, "
             "situação fiscal, existência de ônus ou penhora e regularidade da "
             "construção junto à prefeitura. É uma verificação de poucos dias que "
             "evita disputas de anos."),
            ("Usucapião precisa de processo judicial?",
             "Nem sempre. Desde 2015 existe a via extrajudicial, feita em cartório, "
             "quando não há discordância entre os envolvidos e a documentação "
             "permite. É bem mais rápida. A análise do caso define qual via cabe."),
            ("A construtora atrasou a entrega. O que posso fazer?",
             "Depende do contrato e do tamanho do atraso. As saídas usuais são "
             "exigir a entrega com multa, pedir a rescisão com devolução dos valores "
             "pagos ou negociar um acordo. O primeiro passo é ler o contrato — "
             "principalmente o prazo de tolerância."),
            ("Comprei um imóvel que ainda está no nome do antigo dono. E agora?",
             "Se você tem contrato de compra e venda mas não fez a transferência, o "
             "imóvel juridicamente ainda não é seu. É possível regularizar por "
             "escritura, adjudicação compulsória ou usucapião, conforme o caso."),
        ],
    },
    {
        "slug": "direito-condominial",
        "nome": "Direito Condominial",
        "icone": "condominio",
        "dor": "Inadimplência, convenção desatualizada e conflitos que travam a "
               "administração do condomínio.",
        "resumo": "Assessoria a síndicos, administradoras e condôminos: cobrança, "
                  "convenção, regimento e condução de assembleias.",
        "meta_title": "Advogado de Condomínio em Belo Horizonte",
        "meta_desc": "Cobrança de taxa condominial, convenção, regimento interno e "
                     "assembleias. Assessoria jurídica para síndicos e condôminos em BH.",
        "h1": "Direito Condominial",
        "lead": "Síndico não deveria precisar decidir sozinho o que a lei já resolve. "
                "Damos suporte jurídico para a rotina do condomínio e para os "
                "conflitos que ela produz.",
        "quando": [
            "A inadimplência cresceu e a cobrança amigável não está funcionando",
            "A convenção ou o regimento interno estão desatualizados",
            "Uma assembleia importante precisa ser conduzida sem risco de anulação",
            "Há conflito recorrente entre condôminos ou com o síndico",
            "É necessário notificar ou aplicar penalidade a um condômino",
        ],
        "servicos": [
            ("Cobrança de taxas condominiais", "Cobrança extrajudicial e ação judicial."),
            ("Convenção de condomínio", "Elaboração e revisão conforme a legislação vigente."),
            ("Regimento interno", "Redação de regras aplicáveis e sustentáveis."),
            ("Assessoria a síndicos", "Suporte jurídico para as decisões do dia a dia."),
            ("Assembleias", "Orientação, condução e validação das deliberações."),
            ("Notificações e penalidades", "Aplicação correta das sanções previstas."),
            ("Conflitos entre condôminos", "Mediação e, quando necessário, ação judicial."),
            ("Responsabilidade do condomínio", "Danos em áreas comuns, obras e segurança."),
        ],
        "faq": [
            ("Como cobrar um condômino inadimplente?",
             "O caminho começa pela notificação e pela tentativa de acordo com "
             "parcelamento. Não havendo pagamento, cabe ação de cobrança — a dívida "
             "de condomínio tem execução mais direta do que a maioria das dívidas "
             "civis, o que costuma acelerar o resultado."),
            ("Toda assembleia precisa de advogado?",
             "Não. Mas assembleias que decidem obras de grande valor, alteração de "
             "convenção, destituição de síndico ou aplicação de penalidade grave "
             "são as que mais acabam anuladas por vício de convocação ou quórum. "
             "Nessas, o acompanhamento compensa."),
            ("O condomínio pode multar por barulho?",
             "Pode, desde que a conduta esteja prevista na convenção ou no regimento "
             "e que o procedimento de notificação e defesa seja respeitado. Multa "
             "aplicada sem esse rito costuma cair na Justiça."),
            ("Quem responde por vazamento entre apartamentos?",
             "Depende de onde está a origem. Se o problema está em coluna ou tubulação "
             "de área comum, a responsabilidade é do condomínio; se está dentro da "
             "unidade, é do condômino. A prova técnica define o caso."),
        ],
    },
    {
        "slug": "direito-contratual",
        "nome": "Direito Contratual",
        "icone": "contrato",
        "dor": "Contratos genéricos baixados da internet que só mostram o problema "
               "quando dá errado.",
        "resumo": "Elaboração, revisão e negociação de contratos, além da atuação "
                  "em descumprimento e rescisão.",
        "meta_title": "Advogado de Contratos em Belo Horizonte",
        "meta_desc": "Elaboração, revisão e negociação de contratos civis e "
                     "empresariais. Atuação em descumprimento e rescisão. GR & WMF Advogados.",
        "h1": "Direito Contratual",
        "lead": "Um contrato bem escrito é barato. Um contrato mal escrito só "
                "revela o preço quando a relação azeda.",
        "quando": [
            "Você vai fechar um negócio e precisa de um contrato que proteja o seu lado",
            "Recebeu um contrato pronto e quer saber o que está aceitando",
            "A outra parte descumpriu o combinado",
            "Precisa encerrar um contrato sem pagar multa indevida",
            "Quer padronizar os contratos usados pela sua empresa",
        ],
        "servicos": [
            ("Elaboração de contratos", "Redigidos para o negócio real, não para um modelo genérico."),
            ("Revisão e parecer", "Leitura crítica das cláusulas e dos riscos antes de assinar."),
            ("Negociação", "Apoio técnico durante a negociação das condições."),
            ("Descumprimento contratual", "Cobrança, execução e indenização."),
            ("Rescisão e distrato", "Encerramento com segurança jurídica."),
            ("Contratos de prestação de serviços", "Escopo, prazo, pagamento e responsabilidades."),
            ("Garantias", "Fiança, caução e demais instrumentos de segurança."),
            ("Padronização contratual", "Modelos próprios para uso recorrente da empresa."),
        ],
        "faq": [
            ("Vale a pena usar modelo de contrato da internet?",
             "Como ponto de partida para entender a estrutura, talvez. Como documento "
             "assinado, é arriscado: modelos genéricos costumam faltar exatamente na "
             "cláusula que importa para o seu caso — prazo, multa, rescisão e foro."),
            ("Contrato só vale se for registrado em cartório?",
             "Não. Contrato entre partes capazes, com objeto lícito e forma adequada, "
             "já é válido. O registro serve para dar publicidade e produzir efeito "
             "perante terceiros, o que é relevante em alguns casos específicos."),
            ("A outra parte não cumpriu. Preciso entrar na Justiça?",
             "Nem sempre. Muitas situações se resolvem com notificação extrajudicial "
             "e negociação, especialmente quando há relação comercial a preservar. "
             "A ação judicial entra quando essa via se esgota."),
            ("Posso rescindir um contrato antes do prazo?",
             "Depende do que o contrato prevê. Existem hipóteses de rescisão sem "
             "multa (descumprimento da outra parte, por exemplo) e outras com multa "
             "proporcional. A leitura das cláusulas define o custo da saída."),
        ],
    },
    {
        "slug": "direito-empresarial",
        "nome": "Direito Empresarial",
        "icone": "empresa",
        "dor": "Decisões societárias e riscos jurídicos que crescem junto com a "
               "empresa e ninguém organizou.",
        "resumo": "Constituição e alteração societária, contratos, prevenção de "
                  "riscos e apoio jurídico contínuo ao negócio.",
        "meta_title": "Advogado Empresarial em Belo Horizonte",
        "meta_desc": "Constituição de empresa, alteração societária, contratos e "
                     "consultoria preventiva para empresas em Belo Horizonte. GR & WMF Advogados.",
        "h1": "Direito Empresarial",
        "lead": "A maioria dos problemas jurídicos de uma empresa nasce de decisões "
                "tomadas rápido demais, sem contrato e sem registro. Organizar isso "
                "custa menos do que desfazer.",
        "quando": [
            "Você vai abrir uma empresa ou entrar como sócio em uma existente",
            "A sociedade precisa de um contrato social que reflita a realidade",
            "Um sócio vai sair, entrar ou ter a participação alterada",
            "A empresa precisa de apoio jurídico recorrente, não só quando dá problema",
            "É preciso avaliar riscos antes de um novo contrato ou investimento",
        ],
        "servicos": [
            ("Constituição de empresa", "Escolha do tipo societário e registro."),
            ("Contrato social e alterações", "Regras claras entre sócios, desde o começo."),
            ("Entrada e saída de sócios", "Apuração de haveres e formalização."),
            ("Acordo de sócios", "O que o contrato social não resolve sozinho."),
            ("Contratos empresariais", "Fornecimento, distribuição, parceria e prestação de serviços."),
            ("Consultoria preventiva", "Análise de riscos antes da decisão, não depois."),
            ("Cobrança empresarial", "Recuperação de créditos por via extrajudicial e judicial."),
            ("Adequação à LGPD", "Organização do tratamento de dados na empresa."),
        ],
        "faq": [
            ("Qual tipo de empresa devo abrir?",
             "Depende do número de sócios, do faturamento previsto, da atividade e "
             "do nível de proteção patrimonial desejado. A escolha entre sociedade "
             "limitada e SLU, por exemplo, muda responsabilidades. É uma decisão de "
             "poucos dias que acompanha a empresa por anos."),
            ("Preciso de acordo de sócios se já tenho contrato social?",
             "São documentos diferentes. O contrato social é público e trata da "
             "estrutura. O acordo de sócios é privado e trata do que costuma gerar "
             "briga: entrada de novos sócios, saída, distribuição de lucros, "
             "dedicação e sucessão."),
            ("Sócio pode sair da empresa a qualquer momento?",
             "Em regra sim, mas a forma e o valor a receber dependem do contrato "
             "social e da apuração de haveres. Sem regra escrita, a saída costuma "
             "virar disputa judicial sobre quanto vale a participação."),
            ("O que é consultoria preventiva?",
             "É acompanhar as decisões da empresa antes que virem processo: revisar "
             "contratos, organizar registros societários, avaliar riscos trabalhistas "
             "e ajustar rotinas. Custa uma fração do que custa um litígio."),
        ],
    },
    {
        "slug": "direito-trabalhista",
        "nome": "Direito Trabalhista",
        "icone": "trabalho",
        "dor": "Da rescisão mal feita ao processo que aparece dois anos depois — "
               "para quem contrata e para quem foi contratado.",
        "resumo": "Atuação em reclamações trabalhistas e assessoria preventiva a "
                  "empresas na gestão de riscos e passivos.",
        "meta_title": "Advogado Trabalhista em Belo Horizonte",
        "meta_desc": "Reclamação trabalhista, defesa de empresas, rescisão, verbas e "
                     "consultoria preventiva em Belo Horizonte. GR & WMF Advogados.",
        "h1": "Direito Trabalhista",
        "lead": "Atuamos dos dois lados da relação de trabalho — não no mesmo caso, "
                "evidentemente. Conhecer os dois lados é o que permite antecipar o "
                "argumento do outro.",
        "quando": [
            "Você foi demitido e as verbas rescisórias não foram pagas corretamente",
            "Trabalhou sem registro em carteira ou com função diferente da anotada",
            "Sua empresa recebeu uma reclamação trabalhista",
            "A empresa quer revisar contratos e rotinas para reduzir risco de processo",
            "Houve acidente de trabalho ou doença ocupacional",
        ],
        "servicos": [
            ("Verbas rescisórias", "Conferência do que era devido e cobrança da diferença."),
            ("Reconhecimento de vínculo", "Trabalho sem registro ou com registro incorreto."),
            ("Horas extras e adicionais", "Jornada, insalubridade, periculosidade e noturno."),
            ("Defesa da empresa", "Atuação em reclamações trabalhistas e audiências."),
            ("Consultoria preventiva", "Revisão de contratos, jornada e rotinas de RH."),
            ("Gestão de passivo trabalhista", "Mapeamento de risco e estratégia de acordo."),
            ("Acidente de trabalho", "Estabilidade, indenização e benefício."),
            ("Rescisão e acordos", "Formalização segura para os dois lados."),
        ],
        "faq": [
            ("Qual o prazo para entrar com ação trabalhista?",
             "Em regra, até 2 anos após o fim do contrato, podendo cobrar os últimos "
             "5 anos de direitos do período trabalhado. Perdido esse prazo, o direito "
             "de reclamar se extingue — por isso não convém deixar para depois."),
            ("Trabalhei sem carteira assinada. Tenho direitos?",
             "Sim. O vínculo de emprego se prova pelos fatos: pessoalidade, "
             "habitualidade, subordinação e salário. Havendo prova, o vínculo é "
             "reconhecido e as verbas do período são devidas."),
            ("Como uma empresa reduz risco trabalhista?",
             "Contratos claros, controle de jornada confiável, rescisões bem feitas "
             "e rotina de conferência. A maior parte das condenações vem de falha "
             "de documentação, não de má-fé."),
            ("Acordo trabalhista é sempre ruim para o trabalhador?",
             "Não. Um acordo bem calculado pode trazer, hoje, valor próximo ao que "
             "se receberia anos depois com risco de perda. O que não pode é assinar "
             "sem saber quanto se está abrindo mão — e é aí que o cálculo entra."),
        ],
    },
]

AREAS_POR_SLUG = {a["slug"]: a for a in AREAS}

# ---------------------------------------------------------------- atalhos

# Régua da primeira dobra. A palavra é a que o cliente usa ao procurar, não o
# nome da disciplina — por isso Família aparece como "Divórcio" e "Inventário",
# as duas portas de entrada mais frequentes. Rótulos curtos e de comprimento
# parecido: é o que faz a régua compor como um bloco, e não como uma nuvem.
CHIPS = [
    ("Divórcio", "familia-e-sucessoes"),
    ("Inventário", "familia-e-sucessoes"),
    ("Imóveis", "direito-imobiliario"),
    ("Condomínio", "direito-condominial"),
    ("Contratos", "direito-contratual"),
    ("Empresa", "direito-empresarial"),
    ("Trabalho", "direito-trabalhista"),
]

# ---------------------------------------------------------------- processo

PROCESSO = [
    ("Primeiro contato",
     "Você conta o que está acontecendo pelo WhatsApp, telefone ou formulário. "
     "Respondemos em até 1 dia útil e já indicamos se o caso é da nossa área."),
    ("Consulta e análise",
     "Reunião presencial no Barreiro ou por vídeo. Analisamos os documentos e "
     "explicamos os caminhos possíveis em português, com prós e contras de cada um."),
    ("Proposta de atuação",
     "Você recebe por escrito o escopo do trabalho, as etapas e as condições de "
     "honorários, conforme a tabela da OAB/MG. Sem surpresa depois."),
    ("Condução do caso",
     "Buscamos primeiro a solução consensual quando ela é possível. Não sendo, "
     "seguimos no judicial — sempre com você informado do andamento."),
]

DIFERENCIAIS = [
    ("mediacao", "Acordo antes do processo",
     "Formação em conciliação e mediação. Sempre que o caso permite, buscamos a "
     "solução consensual — costuma ser mais rápida e menos desgastante."),
    ("resposta", "Resposta em 1 dia útil",
     "Você não fica no vácuo esperando retorno. Contato inicial respondido em até "
     "um dia útil, e andamento do caso comunicado sem você precisar cobrar."),
    ("linguagem", "Explicações claras do seu caso",
     "Você vai entender o que está sendo feito, por que está sendo feito e o que "
     "pode acontecer. Sem jargão que só serve para impressionar."),
]

# ---------------------------------------------------------------- FAQ geral

FAQ_GERAL = [
    ("Como funciona a primeira consulta?",
     "Você entra em contato pelo WhatsApp, telefone ou formulário contando "
     "resumidamente o que está acontecendo. Retornamos em até 1 dia útil e "
     "agendamos a consulta, presencial no escritório ou por videochamada. Nela "
     "analisamos os documentos e explicamos os caminhos possíveis."),
    ("O atendimento pode ser online?",
     "Pode. Boa parte dos casos é conduzida por videochamada, e-mail e WhatsApp, "
     "com assinatura eletrônica de documentos. O escritório fica no Barreiro, em "
     "Belo Horizonte, para quem prefere o atendimento presencial."),
    ("Quais documentos devo levar na primeira consulta?",
     "Documento de identidade e tudo que se relacione ao caso: contratos, "
     "certidões, comprovantes, conversas, notificações e processos anteriores. "
     "Se não tiver tudo, venha assim mesmo — parte da consulta é justamente "
     "identificar o que falta."),
    ("Vocês atendem fora de Belo Horizonte?",
     "Sim. Atuamos em Belo Horizonte e região metropolitana, e acompanhamos casos "
     "em outras comarcas de Minas Gerais conforme a necessidade, com apoio de "
     "atendimento remoto."),
    ("Como funcionam os honorários?",
     "Os honorários são definidos caso a caso, conforme a complexidade e o tempo "
     "de trabalho envolvidos, respeitando a Tabela de Honorários da OAB/MG. As "
     "condições são apresentadas por escrito antes do início do trabalho. Como "
     "determina o Código de Ética da advocacia, valores não são divulgados em "
     "site — eles são tratados na consulta."),
    ("Vocês podem garantir o resultado do meu processo?",
     "Não, e desconfie de quem garantir. O Código de Ética da advocacia proíbe "
     "promessa de resultado, e nenhum profissional controla a decisão judicial. "
     "O que apresentamos é uma avaliação honesta das chances, dos riscos e dos "
     "caminhos disponíveis."),
]

# ---------------------------------------------------------------- artigos

ARTIGOS = [
    {
        "slug": "inventario-extrajudicial-como-funciona",
        "titulo": "Inventário extrajudicial: quando dá para resolver em cartório",
        "resumo": "Nem todo inventário precisa de processo judicial. Entenda os "
                  "requisitos da via em cartório, o que ela exige e por que costuma "
                  "ser mais rápida.",
        "area": "familia-e-sucessoes",
        "data": "2026-08-28",
        "data_exibicao": "28 de agosto de 2026",
        "autor": "gabriella-reis-antunes-ferreira",
        "leitura": "5 min",
        "corpo": [
            ("p", "Quando alguém falece, o patrimônio deixado precisa ser formalmente "
                  "transferido aos herdeiros. Esse procedimento é o inventário — e "
                  "muita gente ainda acredita que ele obrigatoriamente corre na Justiça."),
            ("h2", "Os requisitos da via extrajudicial"),
            ("p", "Desde 2007 a legislação permite fazer o inventário diretamente em "
                  "cartório de notas, por escritura pública, desde que três condições "
                  "estejam presentes ao mesmo tempo:"),
            ("ul", ["Todos os herdeiros são maiores de idade e capazes",
                    "Há consenso entre eles quanto à partilha dos bens",
                    "Não existe testamento — ou, havendo, ele já foi judicialmente aberto e autorizado"]),
            ("p", "Faltando qualquer um desses pontos, o inventário precisa ser judicial. "
                  "A presença de advogado é obrigatória nos dois caminhos."),
            ("h2", "Por que a via em cartório costuma ser melhor"),
            ("p", "O inventário extrajudicial não depende da pauta do Judiciário. Reunidos "
                  "os documentos e pago o imposto estadual, a escritura pode ser lavrada "
                  "em poucas semanas. Na via judicial, o mesmo caso pode levar meses ou anos."),
            ("h2", "O prazo que muita gente perde"),
            ("p", "A legislação prevê a abertura do inventário em até 60 dias contados do "
                  "falecimento. Passado esse prazo, incide multa sobre o ITCMD, o imposto "
                  "de transmissão. É o erro mais comum e o mais caro: a família adia por "
                  "luto ou por desentendimento e o custo aumenta."),
            ("h2", "O que fazer se o prazo já passou"),
            ("p", "Ainda é possível regularizar. A multa já incidiu, mas continua correndo "
                  "enquanto nada é feito — e enquanto o inventário não é concluído, nenhum "
                  "bem pode ser vendido ou transferido. Quanto antes o procedimento começar, "
                  "menor o impacto."),
        ],
    },
    {
        "slug": "documentos-para-comprar-imovel-com-seguranca",
        "titulo": "O que conferir antes de assinar a compra de um imóvel",
        "resumo": "A checagem que separa uma compra tranquila de uma disputa de anos "
                  "leva poucos dias. Veja o que precisa ser verificado — e por quê.",
        "area": "direito-imobiliario",
        "data": "2026-08-14",
        "data_exibicao": "14 de agosto de 2026",
        "autor": "gabriella-reis-antunes-ferreira",
        "leitura": "6 min",
        "corpo": [
            ("p", "Comprar imóvel é, para a maioria das famílias, a maior operação "
                  "financeira da vida. Ainda assim, é comum que a análise de documentos "
                  "aconteça depois do sinal pago — quando voltar atrás já custa caro."),
            ("h2", "A matrícula atualizada"),
            ("p", "A matrícula é a certidão de nascimento do imóvel: ela mostra quem é o "
                  "proprietário, o histórico de transferências e todos os ônus registrados "
                  "— hipoteca, penhora, usufruto, indisponibilidade. Deve ser emitida com "
                  "poucos dias de antecedência, porque a situação muda."),
            ("h2", "As certidões do vendedor"),
            ("p", "Um imóvel pode estar limpo e o vendedor não. Dívidas trabalhistas, "
                  "execuções fiscais e ações em andamento podem levar à anulação da venda "
                  "por fraude contra credores, mesmo anos depois. As certidões pessoais do "
                  "vendedor — cível, fiscal, trabalhista e de execuções — protegem o comprador."),
            ("h2", "A situação fiscal do imóvel"),
            ("ul", ["IPTU quitado e sem parcelamento em aberto",
                    "Taxas de condomínio em dia (a dívida acompanha o imóvel, não o antigo dono)",
                    "Contas de consumo sem débito relevante"]),
            ("h2", "A regularidade da construção"),
            ("p", "Construção ou reforma não averbada na matrícula é problema comum. O "
                  "imóvel existe fisicamente, mas juridicamente não — o que impede "
                  "financiamento, dificulta a revenda e pode gerar exigência da prefeitura."),
            ("h2", "O contrato"),
            ("p", "Prazo, forma de pagamento, responsabilidade por despesas, multa por "
                  "descumprimento e condições de rescisão precisam estar escritos. "
                  "Contrato de compra e venda não é formalidade: é o documento que define "
                  "o que acontece se algo der errado."),
        ],
    },
    {
        "slug": "cobranca-de-taxa-condominial-o-que-o-sindico-pode-fazer",
        "titulo": "Inadimplência no condomínio: o que o síndico pode fazer",
        "resumo": "Cobrar é dever do síndico, mas há limites. Entenda o caminho "
                  "correto da cobrança e as práticas que geram condenação.",
        "area": "direito-condominial",
        "data": "2026-07-30",
        "data_exibicao": "30 de julho de 2026",
        "autor": "gabriella-reis-antunes-ferreira",
        "leitura": "4 min",
        "corpo": [
            ("p", "A inadimplência é o problema mais citado por síndicos, e também o que "
                  "mais gera erro de condução. A cobrança é um dever legal do síndico — "
                  "mas a forma como ela é feita pode transformar o condomínio de credor "
                  "em réu."),
            ("h2", "O caminho correto"),
            ("ul", ["Notificação do condômino, com o valor detalhado e prazo para pagamento",
                    "Tentativa de acordo, com parcelamento formalizado por escrito",
                    "Não havendo pagamento, ação de cobrança"]),
            ("p", "A dívida condominial tem tratamento processual mais direto do que a "
                  "maioria das dívidas civis, o que costuma encurtar o caminho até o "
                  "resultado. Também é dívida que acompanha o imóvel: quem compra herda "
                  "o débito."),
            ("h2", "O que não pode ser feito"),
            ("p", "Práticas que expõem o condomínio a condenação por dano moral:"),
            ("ul", ["Divulgar a lista de inadimplentes em mural, elevador ou grupo de mensagens",
                    "Impedir o uso de áreas comuns essenciais ou o acesso à unidade",
                    "Cortar água ou outro serviço essencial da unidade",
                    "Constranger o morador em assembleia"]),
            ("h2", "Restrições que são possíveis"),
            ("p", "A convenção pode prever restrição ao uso de áreas de lazer não "
                  "essenciais e a suspensão do direito de voto do inadimplente em "
                  "assembleia. A diferença está entre restringir um benefício previsto "
                  "em norma e constranger publicamente o devedor."),
        ],
    },
]

ARTIGOS_POR_SLUG = {a["slug"]: a for a in ARTIGOS}
