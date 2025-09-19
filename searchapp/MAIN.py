import tokenizing
import building_posting_list
import doc_vectors
import Dimensionality_reduction
import os

  # FIRSTLY, WE MAKE A FOR LOOP, GIVE THE CORPUS, AND CALL THE FUNCTION PROCESS_FILE FOR EACH FILE
# def process_input(path):
#     """
#     If path is a file -> process that file.
#     If path is a folder -> process all .txt files in it.
#     """
#     if os.path.isfile(path):
#         tokenizing.process_file(path)

#     elif os.path.isdir(path):
#         for filename in os.listdir(path):
#             file_path = os.path.join(path, filename)
#             if os.path.isfile(file_path) and filename.endswith(".txt"):
#                 tokenizing.process_file(file_path)

#     else:
#         print(f"❌ Path not found: {path}")

def main():

  

    # folder_path = "/mnt/c/Users/Sukhraj/Downloads/Corpus/Corpus/query.txt"
    # #RUN ONLY ONCE. ONLY ONCE, ELSE YOUR PICKLE FILE IS GONNA FILL UP VERY FAST
    # tokenizing.process_file(folder_path)

    # okay, so now we have a pickle file with all the tokens of all the files in the corpus
    # now we need to build the posting lists
    # WE NOW DO POSTING LIST CREATION
    building_posting_list.build_postings()

    # PERFECTO ! now, we have to make the vectors. For that we will do scoring now.
    
    doc_vectors.build_doc_vectors()

    #LET US GO. NOW, we want to reduce the dimension of the document vectors, so that we can display it easily. 
    Dimensionality_reduction.reduce_dimension()


if __name__ == "__main__":
    main()
