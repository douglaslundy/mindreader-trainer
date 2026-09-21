# Prompt completo para Claude — revisar e instalar a skill no OpenJarvis

Copie TODO o texto abaixo e entregue ao Claude juntamente com esta pasta/ZIP.

---

Você está operando na minha máquina e deve instalar e validar a skill **mindreader-trainer-v2** no meu OpenJarvis.

## Objetivo

Quero uma instalação segura, verificável e reversível. A skill é um treinador adaptativo baseado no meu material de estudo de *Como Decifrar Mentes*. Ela deve funcionar em conversa multi-turno no agente `orchestrator`.

O comportamento obrigatório de ativação é:

- Quando eu escrever apenas **`/mente`**, a skill deve ser reconhecida e o Jarvis deve abrir um menu com as opções de treinamento e perguntar **“Qual treinamento você deseja iniciar?”**.
- Quando eu escrever um comando específico, por exemplo **`/mente interrogatorio 3`**, o Jarvis deve iniciar diretamente esse modo, sem exibir o menu primeiro.
- Também deve funcionar quando eu disser em linguagem natural algo como **“Use a skill mindreader-trainer-v2 e abra o menu de treinamento.”**

## Restrições

1. NÃO altere o código-fonte do OpenJarvis desnecessariamente.
2. Prefira instalação no escopo de usuário: `~/.openjarvis/skills/mindreader-trainer-v2/`.
3. Antes de substituir uma instalação existente, faça backup com data/hora.
4. Não apague progresso do usuário em `~/.openjarvis/mindreader-trainer-v2/`.
5. Não inclua nem copie para a skill o PDF original do livro; o pacote já contém apenas material transformativo de estudo.
6. Não simplifique nem reescreva os arquivos de conteúdo sem necessidade. Preserve `references/`, `assets/`, `examples/` e `scripts/`.
7. Se encontrar incompatibilidade com a versão instalada do OpenJarvis, adapte apenas o mínimo necessário e documente exatamente o que mudou.

## Etapa 1 — inspeção obrigatória

Antes de instalar:

1. Leia `README.md`, `SKILL.md`, `QUICK_START.txt`, `VERSION` e todos os arquivos em `references/`.
2. Confira `assets/flashcards.jsonl`, `assets/scenario_blueprints.json`, `scripts/progress.py`, `install.sh` e `install.ps1`.
3. Verifique a versão e a instalação local do OpenJarvis, por exemplo com os comandos disponíveis na máquina (`jarvis --help`, `jarvis skill --help`, `jarvis skill list`, ou equivalentes).
4. Confirme que a versão local aceita skills instrucionais baseadas em `SKILL.md` e o diretório de skills do usuário.
5. Se houver configuração customizada de `OPENJARVIS_HOME`, respeite-a.

## Etapa 2 — instalação

Instale a pasta da skill como:

`<OPENJARVIS_HOME ou ~/.openjarvis>/skills/mindreader-trainer-v2/`

Se já existir:

- faça backup antes, por exemplo `mindreader-trainer-v2.backup-AAAAmmdd-HHMMSS`;
- preserve separadamente o diretório de estado/progresso `~/.openjarvis/mindreader-trainer-v2/`;
- substitua apenas a pasta da skill.

No Linux/macOS, você pode usar o `install.sh` após revisá-lo. No Windows, use `install.ps1`. Se optar pela instalação manual, mantenha a mesma estrutura de diretórios.

Garanta permissão de execução para `scripts/progress.py` quando isso for aplicável ao sistema operacional.

## Etapa 3 — validação estrutural

Execute e confira:

`jarvis skill list`

`jarvis skill info mindreader-trainer-v2`

A skill deve aparecer com versão **2.1.0** ou superior compatível, e a descrição deve mencionar que é acionada por `/mente`.

Verifique também que os arquivos abaixo estão presentes após a instalação:

- `SKILL.md`
- `README.md`
- `VERSION`
- `references/BOOK_MAP.md`
- `references/TECHNIQUE_CATALOG.md`
- `references/TRAINING_ENGINE.md`
- `references/SCORING.md`
- `references/SAFETY_AND_EVIDENCE.md`
- `assets/flashcards.jsonl`
- `assets/scenario_blueprints.json`
- `scripts/progress.py`

## Etapa 4 — validação funcional

Use um agente que possa invocar skills, preferencialmente `orchestrator`.

Teste 1 — menu:

Inicie uma sessão de chat e envie exatamente:

`/mente`

Resultado esperado: o Jarvis deve invocar **mindreader-trainer-v2**, mostrar o menu de treinamentos e perguntar qual treinamento eu desejo iniciar. Ele NÃO deve escolher sozinho um exercício antes da minha resposta.

Teste 2 — comando direto:

Envie:

`/mente interrogatorio 1`

Resultado esperado: iniciar diretamente um interrogatório de nível 1; não deve mostrar o menu primeiro.

Teste 3 — encerramento do interrogatório:

Faça 2 ou 3 perguntas ao personagem e depois envie:

`encerrei`

Resultado esperado: o Jarvis deve sair do personagem e fazer a auditoria prevista no `SKILL.md`, separando fatos, inferências, perguntas fortes, inferências não sustentadas e oportunidades perdidas.

Teste 4 — flashcards:

Envie:

`/mente flashcards todos 3`

Resultado esperado: apresentar UM cartão por vez e só revelar/corrigir depois da minha resposta.

Teste 5 — progresso:

Envie:

`/mente progresso`

Resultado esperado: usar a persistência disponível. Se a memória nativa do OpenJarvis não estiver disponível, verificar o fallback em `scripts/progress.py`; se nenhum mecanismo estiver acessível, informar que o progresso vale apenas para a sessão atual.

## Etapa 5 — correção mínima se `/mente` não disparar a skill

Se o texto `/mente` não fizer o agente invocar a skill automaticamente:

1. NÃO altere o core do OpenJarvis de imediato.
2. Confirme se a skill aparece no catálogo do `orchestrator`.
3. Verifique se o frontmatter/description de `SKILL.md` foi carregado corretamente.
4. Garanta que a description declare explicitamente que mensagens iniciadas por `/mente` devem acionar a skill.
5. Reinicie a sessão do Jarvis para forçar nova descoberta do catálogo.
6. Se houver overlays antigos em `~/.openjarvis/learning/skills/mindreader-trainer-v2/` que estejam substituindo a descrição atual, faça backup deles e desative/remova apenas o overlay conflitante, explicando a ação.
7. Se ainda assim a UI/CLI tratar `/...` como comando reservado e não enviar a mensagem ao agente, NÃO faça patch estrutural sem necessidade. Nesse caso, mantenha como invocação oficial alternativa:
   `Use a skill mindreader-trainer-v2 e abra o menu de treinamento.`
   e documente a limitação da interface específica.

## Etapa 6 — relatório final

Ao terminar, entregue um relatório curto contendo:

- versão do OpenJarvis detectada;
- caminho exato em que a skill foi instalada;
- backup criado, se houve;
- resultado de `jarvis skill list` / `skill info`;
- resultado dos cinco testes funcionais;
- qualquer ajuste realizado nos arquivos;
- comando exato para iniciar o Jarvis;
- comando principal para chamar a skill: **`/mente`**;
- fallback em linguagem natural, se necessário.

Não considere a tarefa concluída apenas porque os arquivos foram copiados. Conclua somente depois da validação funcional ou depois de explicar objetivamente qual limitação da instalação local impediu o teste.

---
