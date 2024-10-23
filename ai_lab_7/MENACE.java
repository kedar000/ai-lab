import java.util.*;

public class MENACE {
    // A map of game states to available moves
    private Map<String, Map<Integer, Integer>> gameStateBoxes;
    private Random random;

    // Counters for results
    private int wins;
    private int losses;
    private int draws;

    public MENACE() {
        this.gameStateBoxes = new HashMap<>();
        this.random = new Random();
        this.wins = 0;
        this.losses = 0;
        this.draws = 0;
    }

    // Get the next move based on current game state
    public int getNextMove(String currentState) {
        
        if (!gameStateBoxes.containsKey(currentState)) {
            initializeState(currentState);
        }

        Map<Integer, Integer> possibleMoves = gameStateBoxes.get(currentState);
        if (possibleMoves == null || possibleMoves.isEmpty()) {
            throw new IllegalStateException("No available moves for state: " + currentState);
        }

        // Create a weighted list of moves
        List<Integer> weightedMoves = new ArrayList<>();
        for (Map.Entry<Integer, Integer> entry : possibleMoves.entrySet()) {
            int move = entry.getKey();
            int weight = entry.getValue();
            for (int i = 0; i < weight; i++) {
                weightedMoves.add(move);
            }
        }

        return weightedMoves.get(random.nextInt(weightedMoves.size()));
    }

    // Initialize a new game state with default possible moves and weights
    private void initializeState(String state) {
        Map<Integer, Integer> possibleMoves = new HashMap<>();
        for (int i = 0; i < 9; i++) {
            if (state.charAt(i) == '.') {
                possibleMoves.put(i, 3);
            }
        }
        gameStateBoxes.put(state, possibleMoves);
    }

    // Reinforce the machine based on game outcome
    public void reinforce(String state, int move, String result) {
        Map<Integer, Integer> moves = gameStateBoxes.get(state);
        if (moves != null && moves.containsKey(move)) {
            if ("win".equals(result)) {
                moves.put(move, moves.get(move) + 1);
            } else if ("lose".equals(result)) {
                moves.put(move, Math.max(moves.get(move) - 1, 1));
            } else if ("draw".equals(result)) {
                moves.put(move, moves.get(move) + 1);
            }
        }
    }

    // Simulate a full game between MENACE and a random opponent
    public void playGame() {
        String currentState = "........."; // Start with an empty board
        List<String> states = new ArrayList<>();
        List<Integer> moves = new ArrayList<>();
        boolean menaceTurn = true;

        System.out.println("<-----------Starting new game!------------>");
        printBoard(currentState);

        while (!isGameOver(currentState)) {
            if (menaceTurn) {
                int move = getNextMove(currentState);
                states.add(currentState);
                moves.add(move);
                currentState = applyMove(currentState, move, 'X');
                System.out.println("MENACE makes move:");
            } else {
                // Random opponent move
                List<Integer> availableMoves = getAvailableMoves(currentState);
                int move = availableMoves.get(random.nextInt(availableMoves.size()));
                currentState = applyMove(currentState, move, 'O');
                System.out.println("Random opponent makes move:");
            }

            printBoard(currentState);
            menaceTurn = !menaceTurn;
        }

        // Determine the result and reinforce MENACE
        String result = getResult(currentState);
        for (int i = 0; i < states.size(); i++) {
            reinforce(states.get(i), moves.get(i), result);
        }

        System.out.println("Game result: " + result);

        // Update counters
        if ("win".equals(result)) {
            wins++;
        } else if ("lose".equals(result)) {
            losses++;
        } else if ("draw".equals(result)) {
            draws++;
        }
    }

    // Check if the game is over
    private boolean isGameOver(String state) {
        return getResult(state) != null || !state.contains(".");
    }

    // Apply a move to the current state
    private String applyMove(String state, int move, char player) {
        char[] chars = state.toCharArray();
        chars[move] = player;
        return new String(chars);
    }

    // Get the list of available moves from the current state
    private List<Integer> getAvailableMoves(String state) {
        List<Integer> availableMoves = new ArrayList<>();
        for (int i = 0; i < state.length(); i++) {
            if (state.charAt(i) == '.') {
                availableMoves.add(i);
            }
        }
        return availableMoves;
    }

    // Determine the result of the game
    private String getResult(String state) {
        String[] winningPatterns = {
                "012", "345", "678", // Rows
                "036", "147", "258", // Columns
                "048", "246"         // Diagonals
        };
        for (String pattern : winningPatterns) {
            char first = state.charAt(pattern.charAt(0) - '0');
            if (first != '.' && first == state.charAt(pattern.charAt(1) - '0') && first == state.charAt(pattern.charAt(2) - '0')) {
                return (first == 'X') ? "win" : "lose";
            }
        }

        // Check if the board is full and no one has won — this is a draw
        if (!state.contains(".")) {
            return "draw";
        }

        return null;
    }

    // Print the current state of the Tic-tac-toe board
    private void printBoard(String state) {
        for (int i = 0; i < 9; i += 3) {
            System.out.println(state.charAt(i) + " | " + state.charAt(i + 1) + " | " + state.charAt(i + 2));
        }
        System.out.println();
    }

    // Print the final tally of wins, losses, and draws
    private void printResults() {
        System.out.println("Final Results:");
        System.out.println("MENACE Wins: " + wins);
        System.out.println("MENACE Losses: " + losses);
        System.out.println("Draws: " + draws);
    }

    public static void main(String[] args) {
        MENACE menace = new MENACE();
        // Simulate 5 games and display results
        for (int i = 0; i < 5; i++) {
            menace.playGame();
        }

        // Print final win/loss/draw tally
        menace.printResults();
    }
}