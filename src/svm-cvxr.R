require(CVXR)
require(caret)

#install.packages('caret', dependencies = TRUE)
#install.packages('e1071', dependencies=TRUE)

build_relationship <- function(dataset) {

  pairs <- list()
  index <- 0

  for(i in 1:nrow(dataset)){

      queryid_current <- dataset[[2]][[i]]

      for(j in 1:nrow(dataset)){

          queryid_loop <- dataset[[2]][[j]]

          if(queryid_current == queryid_loop && j > i){
              index <- index + 1
              pairs[[index]] <- c(i, j)
          }

      }

  }
  pairs
}

get_entities_of_documents <- function(documents) {
  con = file("dataset/doc-ent-relationship.txt", "r")
  all_entities = c()
  while ( TRUE ) {

    line = readLines(con, n = 1)

    if ( length(line) == 0 ) {
      break
    }

    entities = as.integer(unlist(strsplit(line,",")))

    for(i in 1:length(documents)) {
      # Make sure it is the document
      if(documents[i] == entities[1]){
        all_entities <- c(all_entities, entities[-1])
      }
    }

  }

  close(con)

  all_entities
}


get_entities_of_documents_id <- function(id) {
  con = file("dataset/doc-ent-relationship.txt", "r")
  all_entities = c()
  while ( TRUE ) {

    line = readLines(con, n = 1)

    if ( length(line) == 0 ) {
      break
    }

    entities = as.integer(unlist(strsplit(line,",")))

    if(entities[1] == id) {
       all_entities <- c(all_entities, entities[-1])
       break
    }

  }

  close(con)

  all_entities
}


# Return an all restrictions list
f_constraints <- function(w, relationship, dataset, slack) {

  result <- list()

  for (pairs in relationship) {

    query1_doc1 <- dataset[pairs[1],]
    query1_doc2 <- dataset[pairs[2],]

    expression  <- w %*% query1_doc1 >=  w %*% query1_doc2 + 1 - sum(slack)
    result      <- c(result, expression)
  }

  result
}

# Calculate the document punctuation using linear kernel
calc_pont_doc <- function(doc, w){
  kernel <- sum(doc * w) # Linear Kernel
  # kernel <- 1 + sum(doc * w)^3 # Polynomial Kernel
  # kernel <- exp(-0.7 * sum((doc - w^2))) # Radial Basis Function Kernel 
  kernel
}

# Solve convex optmization problem according the papper: OPTIMIZING SEARCH ENGINES USING CLICKTHOUGH DATA
calculate_optimal_w_cvxr <- function(dataset, relationship) {
    c           <- 1
    ncols       <- ncol(dataset)
    w           <- Variable(cols = ncols)
    slack       <- Variable(cols = length(relationship))
    objective   <- Minimize(1/2 * sum_squares(vstack(w, w)) + c * sum(slack))
    constraints <- f_constraints(w, relationship, dataset, slack)
    problem     <- Problem(objective, constraints)
    solution    <- solve(problem, solver = "SCS")
    optimal_w   <- solution$getValue(w)
    optimal_w
}

get_features <- function(dataset) {
  dataset[1:3] <- list(NULL)
  apply(dataset, 2, as.numeric)
}

fit <- function() {

  dataset                 <- read.table("dataset/features-normalized-tranning", header=TRUE);
  doc_query_relationship  <- build_relationship(dataset);
  features                <- get_features(dataset)
  optimal_w               <- calculate_optimal_w_cvxr(features, doc_query_relationship);

  write.table(optimal_w, "dataset/trained-optmal.txt", eol="\n", row.names=FALSE, col.names=FALSE)

  print(optimal_w)

}

predict <- function() {

  optimal_w    <- read.table("dataset/trained-optmal.txt",header = FALSE, sep = " ", dec = ".")
  dataset      <- read.table("dataset/features-normalized-test", header=TRUE)
  features     <- get_features(dataset)
  nrow_dataset <- length(dataset[,1])
  ncol_dataset <- length(dataset[1,])
  result       <- matrix(0, nrow = nrow_dataset, ncol = 3)

  doc_query <- dataset
  doc_query[1] <- list(NULL)
  doc_query[3:ncol_dataset] <- list(NULL)

  query_id    <- dataset[1,2]

  for(i in 1:nrow_dataset) {

    if(query_id != dataset[i,2]){
      query_id <- dataset[i,2]
    }

    result[i,1] <- query_id  #query_id
    result[i,2] <- dataset[i,3] #doc_id
    result[i,3] <- calc_pont_doc(features[i,], optimal_w) #ponctuation

  }

  result <- result[order(result[,1], -result[,3]),]
  result <- result[,-3]
  mx <- confusionMatrix(table(doc_query[,2], result[,2]))

}