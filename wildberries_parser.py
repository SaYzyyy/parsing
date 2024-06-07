import requests
import lxml
import json
from time import gmtime, strftime

def collect_data(price1):
	
	headers = {
		'Accept': '*/*',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
	}
	prod_dict = []
	for pages in range(1, 61):
		url = f"https://catalog.wb.ru/catalog/electronic14/v2/catalog?appType=1&cat=9468&curr=rub&dest=-1257786&page={pages}&sort=popular&spp=30"

		resp = requests.get(url=url, headers=headers)

		if resp.status_code != 200:
			print('Странице плохо, переходим на следующую...')
		else:
			with open(f'res_{pages}.json', 'w', encoding='utf-8') as file:
				json.dump(resp.json(), file, indent=4, ensure_ascii=False)

			with open(f'res_{pages}.json', 'r', encoding='utf-8') as file1:
				data = json.load(file1)
				# print(data)

			data1 = data['data']

			products = data1.get('products')

			for p in products:
				p_rev_rating = p.get('reviewRating')
				p_name = p.get('name').strip()
				p_brand = p.get('brand').strip()
				p_id = p.get('id')
				p_brandid = p.get('brandId')
				p_sizes = p.get('sizes')
				for s in p_sizes:
					price = s.get('price')
					pricespl1 = str(price).split(':')
					pricespl2 = str(pricespl1).split(',')
					pricespl3 = str(pricespl2).split(' ')
					if (p_rev_rating >= 4.7) and ((int(pricespl3[8][:-4])) <= price1):
						prod_dict.append(
							{
								'Ссылка': f'https://www.wildberries.ru/catalog/{p_id}/detail.aspx',
								'Название': p_name,
								'Магазин': p_brand,
								'ID магазина': p_brandid,
								'Цена без скидки': f'{pricespl3[3][:-4]} рублей',
								'Цена со скидкой': f'{pricespl3[8][:-4]} рублей',
								'Рейтинг': p_rev_rating
							}
						)


			print(f'\n\n\n{strftime("%Y-%m-%d %H:%M:%S", gmtime())}')
			print(f'[INFO!] Итерация {pages} завершилась успешно!')
			print(url)		
			print(resp)
			print('__________________________________________________\n\n\n')
	print(prod_dict)
	with open('result.json', 'w', encoding='utf-8') as file:
		json.dump(prod_dict, file, indent=4, ensure_ascii=False)

def main():
	collect_data()

if __name__ == '__main__':
	main()
