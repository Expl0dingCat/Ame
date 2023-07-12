from hyperdb import HyperDB

class memory:
    def __init__(self, docs=None) -> None:
        self.db = HyperDB(docs)
    
    def save_memory(self, db_path):
        self.db.save(db_path)
    
    def get_docs(self):
        return self.db.dict()

    def memorize(self, memory):
        self.db.add_documents(memory)

    def load_memory(self, db_path):
        self.db.load(db_path)

    def remember(self, query):
        lst = self.get_docs()
        # Get the highest likelihood memory
        results = self.db.query(query, top_k=1, return_similarities=False)
        # Get the 2 memories before and after the highest likelihood memory for context
        memory = results[0]

        start_index = next((i for i, d in enumerate(lst) if d['document'] == memory), None)

        if start_index is not None:
            prev_count = 1
            post_count = 1

            start = max(start_index - prev_count, 0)
            end = min(start_index + post_count + 1, len(lst))

            result = [lst[i]['document'] for i in range(start, end)]
            return result
        else:
            return f"Something went wrong. Could not find memory in memory database. {memory}"

if __name__ == '__main__':
    print('This is a handler, it is not meant to be run directly.')
    pass