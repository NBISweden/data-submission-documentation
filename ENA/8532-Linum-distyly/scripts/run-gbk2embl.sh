python3 ./gbk2embl.py -i Genbank/Laustriacum.gb --project_id PRJEB108312 --locus_tag LAUSTCHL --species "Linum austriacum" -o Embl-gb/Laustriacum.embl 
python3 ./gbk2embl.py -i Genbank/Lbienne.gb --project_id PRJEB108312 --locus_tag LBIENCHL --species "Linum bienne" -o Embl-gb/Lbienne.embl 
python3 ./gbk2embl.py -i Genbank/Lcampanulatum.gb --project_id PRJEB108312 --locus_tag LCAMPCHL --species "Linum campanulatum" -o Embl-gb/Lcampanulatum.embl 
python3 ./gbk2embl.py -i Genbank/Lcapitatum.gb --project_id PRJEB108312 --locus_tag LCAPICHL --species "Linum capitatum" -o Embl-gb/Lcapitatum.embl 
python3 ./gbk2embl.py -i Genbank/Lflavum.gb --project_id PRJEB108312 --locus_tag LFLAVCHL --species "Linum flavum" -o Embl-gb/Lflavum.embl 
python3 ./gbk2embl.py -i Genbank/Lgrandiflorum_thrum.gb --project_id PRJEB108312 --locus_tag LGRANCHL --species "Linum grandiflorum" -o Embl-gb/Lgrandiflorum_thrum.embl 
python3 ./gbk2embl.py -i Genbank/Lhirsutum.gb --project_id PRJEB108312 --locus_tag LHIRSCHL --species "Linum hirsutum" -o Embl-gb/Lhirsutum.embl 
python3 ./gbk2embl.py -i Genbank/Lleonii.gb --project_id PRJEB108312 --locus_tag LLEOCHL --species "Linum leonii" -o Embl-gb/Lleonii.embl 
python3 ./gbk2embl.py -i Genbank/Lmaritimum_thrum.gb --project_id PRJEB108312 --locus_tag LMARICHL --species "Linum maritimum" -o Embl-gb/Lmaritimum_thrum.embl 
python3 ./gbk2embl.py -i Genbank/Lnarbonense.gb --project_id PRJEB108312 --locus_tag LNARBCHL --species "Linum narbonense" -o Embl-gb/Lnarbonense.embl 
python3 ./gbk2embl.py -i Genbank/Lperenne.gb --project_id PRJEB108312 --locus_tag LPERECHL --species "Linum perenne" -o Embl-gb/Lperenne.embl 
python3 ./gbk2embl.py -i Genbank/Lsuffruticosum_thrum.gb --project_id PRJEB108312 --locus_tag LSUFFCHL --species "Linum suffruticosum" -o Embl-gb/Lsuffruticosum_thrum.embl 
python3 ./gbk2embl.py -i Genbank/Ltauricum.gb --project_id PRJEB108312 --locus_tag LTAURCHL --species "Linum tauricum" -o Embl-gb/Ltauricum.embl 
python3 ./gbk2embl.py -i Genbank/Lteniufolium.gb --project_id PRJEB108312 --locus_tag LTENUICHL --species "Linum tenuifolium" -o Embl-gb/Lteniufolium.embl 
python3 ./gbk2embl.py -i Genbank/Ltenue.gb --project_id PRJEB108312 --locus_tag LTENUECHL --species "Linum tenue" -o Embl-gb/Ltenue.embl 
python3 ./gbk2embl.py -i Genbank/Lthracicum.gb --project_id PRJEB108312 --locus_tag LTHRACHL --species "Linum thracicum" -o Embl-gb/Lthracicum.embl 
python3 ./gbk2embl.py -i Genbank/Ltrigynum.gb --project_id PRJEB108312 --locus_tag LTRIGCHL --species "Linum trigynum" -o Embl-gb/Ltrigynum.embl 
gzip -k Embl-gb/*.embl
