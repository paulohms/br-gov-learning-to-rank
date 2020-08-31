library("spacyr")

# spacy_install()
# spacy_download_langmodel("pt")

BASE_DIR = $PATH

spacy_initialize(model = "pt")

folders <- dir(BASE_DIR)

for(folder in folders) {

    dataset <- paste(BASE_DIR,folder,"/metadata.txt", sep="")

    if(file.exists(dataset)) {

        dataset_text <- readLines(dataset)
        entities <- spacy_extract_entity(dataset_text, type="named", multithread = TRUE)

        for(i in 1:nrow(entities)) {

            if(entities$ent_type[i] == "PER" || entities$ent_type[i] == "ORG"){
                write(paste(folder, entities$text[i], sep = " | "),file="all-entities.txt",append=TRUE)
            }

        }

        write("\n",file="all-entities.txt",append=TRUE)

    }

}
