#!/usr/bin/env lua

-- Tabela de cores ANSI para criar o visual "2D" no terminal KDE (Konsole)
local C = {
    reset = "\27[0m",
    bold = "\27[1m",
    cyan = "\27[1;36m",
    green = "\27[1;32m",
    yellow = "\27[1;33m",
    purple = "\27[1;35m",
    red = "\27[1;31m",
    bg_dark = "\27[40m"
}

-- Função para limpar a tela e montar o cabeçalho
local function render_header()
os.execute("clear")
print(C.cyan .. C.bold .. "================================================================" .. C.reset)
print(C.purple .. C.bold .. "  🚀 GERADOR DE PROJETOS QML / PYSIDE6 / C++" .. C.reset)
print(C.cyan .. C.bold .. "================================================================" .. C.reset)
print("")
end

-- Função para capturar o nome do projeto
local function get_project_name(arg_name)
if arg_name and arg_name ~= "" then
    return arg_name
    end

    io.write(C.green .. "📂 Digite o nome do projeto (padrão: qt6_app): " .. C.reset)
    local input = io.read()

    if input == nil or input == "" then
        return "qt6_app"
        end
        return input
        end

        -- Função para exibir e capturar a escolha do template
        local function get_template_choice(arg_template)
        if arg_template and arg_template ~= "" then
            return arg_template
            end

            print("\n" .. C.yellow .. "🌟 Selecione o Template de Projeto para Qt6:" .. C.reset)
            print(C.cyan .. "----------------------------------------------------------------" .. C.reset)
            print(C.bold .. "  1) " .. C.reset .. "PySide6 MVC (Widgets) - [Padrão/Elite]")
            print(C.bold .. "  2) " .. C.reset .. "PySide6 Qt Quick (QML)")
            print(C.bold .. "  3) " .. C.reset .. "PySide6 Qt Designer (.ui)")
            print(C.bold .. "  4) " .. C.reset .. "C++ Qt Quick (QML + CMake)")
            print(C.bold .. "  5) " .. C.reset .. "C++ Qt Widgets (.ui + CMake)")
            print(C.cyan .. "----------------------------------------------------------------" .. C.reset)

            io.write(C.green .. "👉 Digite a opção (1-5) [1]: " .. C.reset)
            local input = io.read()

            if input == nil or input == "" then
                return "1"
                end
                return input
                end

                -- Lógica Principal
                render_header()

                -- Pega os argumentos passados via linha de comando (se houver)
                local arg_project = arg[1]
                local arg_template = arg[2]

                local project_name = get_project_name(arg_project)
                local template_type = get_template_choice(arg_template)

                print("\n" .. C.cyan .. "⚙️  Configurando projeto: " .. C.yellow .. project_name .. C.cyan .. " com template " .. C.yellow .. template_type .. C.reset)

                -- Descobre o diretório atual onde o script Lua está rodando
                local handle = io.popen("pwd")
                local current_dir = handle:read("*a"):gsub("%s+", "")
                handle:close()

                local python_script = current_dir .. "/generator.py"

                -- Monta o comando conectando Lua com o Python
                local command = string.format('python3 "%s" "%s" "%s"', python_script, project_name, template_type)

                print(C.purple .. "🚀 Executando: " .. C.reset .. command .. "\n")

                -- Executa o Python e repassa o controle
                local result = os.execute(command)

                if not result then
                    print(C.red .. "❌ Erro ao executar o gerador Python." .. C.reset)
                    else
                        print("\n" .. C.green .. "✅ Projeto criado com sucesso!" .. C.reset)
                        end
end


local function get_template_choice_interativo()
print("\n" .. C.yellow .. "🌟 Selecione o Template com as setas do teclado:" .. C.reset)

-- Chama o Gum pelo Lua para criar o menu 2D
local cmd = [[gum choose \
"1_PySide6_MVC_(Widgets)" \
"2_PySide6_Qt_Quick_(QML)" \
"3_PySide6_Qt_Designer" \
"4_C++_Qt_Quick_(QML_CMake)" \
"5_C++_Qt_Widgets"]]

local handle = io.popen(cmd)
local choice = handle:read("*a"):gsub("%s+", "")
handle:close()

-- Extrai apenas o primeiro número da string escolhida
local option_number = choice:sub(1, 1)

if option_number == "" then return "1" end
    return option_number
end
