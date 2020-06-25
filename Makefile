protein_domains_vs_string_degree.png : generate_figure.py proteins_w_domains.txt data.txt
	python3 generate_figure.py

data.txt : 
	curl -o 9606.protein.links.v11.0.txt.gz https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz
	gunzip 9606.protein.links.v11.0.txt.gz
	awk ' $$3 >=500 ' 9606.protein.links.v11.0.txt > data.txt

.PHONY : clean
clean :
	rm -f data.txt
	rm -f protein_domains_vs_string_degree.png
