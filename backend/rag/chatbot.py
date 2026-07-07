from backend.rag.rag_pipeline import generate_answer


def chat(question: str):

    answer, sources = generate_answer(question)

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":

    while True:

        question = input("\nYou : ")

        if question.lower() == "exit":
            break

        response = chat(question)

        print("\nMedIntel AI:\n")
        print(response["answer"])

        print("\nSources:")

        for source in response["sources"]:
            print("-", source)