import pandas as pd
from botcity.web import WebBot, Browser, By
from botcity.web.browsers.firefox import default_options
from botcity.core import DesktopBot

user_dir = r"C:\Users\Master\AppData\Roaming\Mozilla\Firefox\Profiles\igapdwaz.default-release"

entrada = 'Você poderia gerar no formato JSON com o nome "produtos" os dados de 3 produtos eletronicos contendo as informações de nome, categoria, codigo, identificador, descrição, preço e quantidade?'


def coleta_dados_produtos():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.FIREFOX
    bot.driver_path= r"D:\Code\Python\DIO\BOT\geckodriver.exe"
    
    def_options = default_options(headless=False, user_data_dir=user_dir)
    bot.options = def_options

    bot.browse("https://flowgpt.com/chat")
    bot.maximize_window()
    bot.wait(2000)

    input_texto = bot.find_element(
        selector="#scrollableDiv > div.overflow-hidden.w-full.h-full.relative.css-0 > div.hidden.sm\:block.h-full > div > div.flex.flex-col.h-full.w-full.relative > div.relative.flex-shrink-0.mt-4 > div.flex.items-center.max-w-\[800px\].mx-auto.mb-2.w-full.relative.text-white.bg-white.rounded-\[10px\] > textarea",
        by=By.CSS_SELECTOR
    )
    input_texto.send_keys(entrada)

    botao_enviar = bot.find_element(
        selector='#scrollableDiv > div.overflow-hidden.w-full.h-full.relative.css-0 > div.hidden.sm\:block.h-full > div > div.flex.flex-col.h-full.w-full.relative > div.relative.flex-shrink-0.mt-4 > div.flex.items-center.max-w-\[800px\].mx-auto.mb-2.w-full.relative.text-white.bg-white.rounded-\[10px\] > button > svg > path',
        by=By.CSS_SELECTOR
    )
    botao_enviar.click()
    bot.wait(20000)

    while botao_enviar.get_attribute("disabled") == "true":
        print("Aguardando...")
        bot.wait(30000)

    dados = bot.find_element("language-json", By.CLASS_NAME).get_attribute("textContent")
    print(dados)
    
    dados = pd.read_json(dados)
    df =pd.json_normalize(dados['produtos'])
    print(df)

    df.to_excel("produtos.xlsx", index=False)

    bot.wait(20000)
    bot.stop_browser()

    return df

def cadastra_produtos(dataframe: pd.DataFrame):
    bot = DesktopBot()

    bot.execute(r"D:\Program Files\Fakturama\Fakturama.exe")


def main():
    dados_produtos = coleta_dados_produtos()
    cadastra_produtos(dados_produtos)

if __name__ == '__main__':
    main()