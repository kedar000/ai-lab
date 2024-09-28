import re
import heapq

# Text Preprocessing
def preprocess_content(content):
    content = content.lower()
    content = re.sub(r'[^\w\s]', '', content)
    sentence_list = re.split(r'(?<=[.!?]) +', content)  # Split into sentences
    return [s.strip() for s in sentence_list if s.strip()]

# Levenshtein Distance Function
def levenshtein_dist(string1, string2):
    if len(string1) < len(string2):
        return levenshtein_dist(string2, string1)

    if len(string2) == 0:
        return len(string1)

    prev_row = range(len(string2) + 1)
    for index, char1 in enumerate(string1):
        curr_row = [index + 1]
        for j, char2 in enumerate(string2):
            insert_cost = prev_row[j + 1] + 1
            delete_cost = curr_row[j] + 1
            substitute_cost = prev_row[j] + (char1 != char2)
            curr_row.append(min(insert_cost, delete_cost, substitute_cost))
        prev_row = curr_row

    return prev_row[-1]

# A* Search Algorithm
def a_star_search(doc_a, doc_b):
    initial_state = (0, 0)
    target_state = (len(doc_a), len(doc_b))
    
    open_list = []
    heapq.heappush(open_list, (0, initial_state))
    parent_map = {}
    g_score_map = {initial_state: 0}
    
    while open_list:
        current_f, current_state = heapq.heappop(open_list)
        i, j = current_state
        
        if current_state == target_state:
            return reconstruct_trace(parent_map, current_state)

        # Align sentences
        if i < len(doc_a) and j < len(doc_b):
            cost = levenshtein_dist(doc_a[i], doc_b[j])
            neighbor = (i + 1, j + 1)
            tentative_g_score = g_score_map[current_state] + cost
            if neighbor not in g_score_map or tentative_g_score < g_score_map[neighbor]:
                parent_map[neighbor] = current_state
                g_score_map[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(doc_a, doc_b, neighbor)
                heapq.heappush(open_list, (f_score, neighbor))

        # Skip sentences in document A
        if i < len(doc_a):
            neighbor = (i + 1, j)
            tentative_g_score = g_score_map[current_state] + 1
            if neighbor not in g_score_map or tentative_g_score < g_score_map[neighbor]:
                parent_map[neighbor] = current_state
                g_score_map[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(doc_a, doc_b, neighbor)
                heapq.heappush(open_list, (f_score, neighbor))

        # Skip sentences in document B
        if j < len(doc_b):
            neighbor = (i, j + 1)
            tentative_g_score = g_score_map[current_state] + 1
            if neighbor not in g_score_map or tentative_g_score < g_score_map[neighbor]:
                parent_map[neighbor] = current_state
                g_score_map[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(doc_a, doc_b, neighbor)
                heapq.heappush(open_list, (f_score, neighbor))

    return None  # No path found

def heuristic(doc_a, doc_b, state):
    i, j = state
    return abs(len(doc_a) - i) + abs(len(doc_b) - j)

def reconstruct_trace(parent_map, current):
    path = [current]
    while current in parent_map:
        current = parent_map[current]
        path.append(current)
    return path[::-1]

# Function to read file content
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

# Plagiarism Detection
def detect_plagiarism(doc_a_path, doc_b_path):
    doc_a_text = read_file(doc_a_path)
    doc_b_text = read_file(doc_b_path)

    if doc_a_text is None or doc_b_text is None:
        return

    doc_a = preprocess_content(doc_a_text)
    doc_b = preprocess_content(doc_b_text)

    alignment = a_star_search(doc_a, doc_b)
    if alignment is None:
        print("No alignment found.")
        return

    for i, j in alignment:
        if i < len(doc_a) and j < len(doc_b):
            distance = levenshtein_dist(doc_a[i], doc_b[j])
            print(f"Edit Distance: {distance}")

# Test Cases
if __name__ == "__main__":
    # Replace with the paths to your document files
    doc1_path = "./test-1/doc1"
    doc2_path = "./test-1/doc1"
    print("Identical files:")
    detect_plagiarism(doc1_path, doc2_path)
    
    print("")
    
    test_2_doc_1 = "./test-2/doc1"
    test_2_doc_2 = "./test-2/doc2"
    print("Slightly modified document:")
    detect_plagiarism(test_2_doc_1, test_2_doc_2)
    
    test_3_doc_1 = "./test-3/doc1"
    test_3_doc_2 = "./test-3/doc2"
    print("")
    
    print("Completely Different Documents:")
    detect_plagiarism(test_3_doc_1, test_3_doc_2)
