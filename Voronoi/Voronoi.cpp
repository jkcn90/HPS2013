// Voronoi.cpp : Defines the entry point for the console application.
//
#include <vector>
#include <iostream>
#include <istream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <math.h>
#include <stdio.h>
#include <string.h>

#define IS_ZERO(x) (x > -0.000001 && x < 0.000001)
#define PI 3.14159265

struct Move {
	int playerNum;
	int x;
	int y;
};

typedef std::vector<Move*> MovesType;

MovesType moves, testMoves;
int movesNum = 0;
//int player1Score = 0;
//int player2Score = 0;
int playerScores[20];
int currPlayer = 0;
int totalPlayers = 0;
int outX = 0;
int outY = 0;
std::string outputString;
double matrices[20][1000][1000];

//double matrix1[1000][1000];
//double matrix2[1000][1000];

void outputFile(const char *fileName)
{
	//std::ofstream f;
	//f.open(fileName);
	//f << outputString << std::endl;
	std::cout << outputString;

	//f.close();
}

void parseTestMoves(std::string &line)
{

	char *str = new char[line.length() + 1];
	strcpy(str, line.c_str());
	char *pch = strtok(str, ",");
	while (pch != NULL)
	{
		int x = atoi(pch);
		pch = strtok(NULL, ",");
		int y = atoi(pch);
		Move *m = new Move();
		m->playerNum = currPlayer;
		m->x = x;
		m->y = y;
		testMoves.push_back(m);
		pch = strtok(NULL, ",");
	}
}

void parseMoves(std::string &line)
{
	// numberOfPlayers, playerId, numberOfMoves
//playerOneMoves
//playerTwoMoves
//.... playerNMoves

	char *str = new char[line.length() + 1];
	strcpy(str, line.c_str());
	char *pch = strtok(str, ",");
	totalPlayers = atoi(pch);
	pch = strtok (NULL, ",");
	currPlayer = atoi(pch);
	pch = strtok (NULL, ",");
	int numberOfMoves = atoi(pch);
	
	pch = strtok (NULL, ",");
	while (pch != NULL)
	{
		Move *m = new Move();
		m->playerNum = atoi(pch);
		pch = strtok (NULL, ",");
		m->x = atoi(pch);
		pch = strtok (NULL, ",");
		m->y = atoi(pch);
		moves.push_back(m);
		pch = strtok (NULL, ",");
	}
	movesNum = moves.size();
}

void parseFile(const char *fileName)
{
	//std::ifstream input(fileName);
	std::string line1, line2;

	std::getline(std::cin, line1);
	std::getline(std::cin, line2);
	//input.close();
	
	parseMoves(line2);
	parseTestMoves(line1);

}

double distance(int x1, int y1, int x2, int y2)
{
	double d = sqrt(pow((double)(x1 - x2), 2) + pow((double)(y1 - y2), 2));
	return d;
}

void calculatePullForPoint(int x, int y)
{
	double pull;
	long deltaX, deltaY;
	for (int i=0; i<moves.size(); ++i)
	{
		deltaX = moves[i]->x - x;
		deltaX = deltaX * deltaX;
		deltaY = moves[i]->y - y;
		deltaY = deltaY * deltaY;
		if (deltaX > 0 || deltaY > 0)
		{
			pull = 1.0 / (deltaX + deltaY);
		}
		else
		{
			pull = 1000000;	// infinity approximation
		}
		/*if (moves[i]->playerNum == 1)
		{
			matrix1[x][y] += pull;
		}
		else
		{
			matrix2[x][y] += pull;
		}*/
		matrices[moves[i]->playerNum-1][x][y] += pull;
	}
}

void calculateCurrentMoves()
{
	for (int x=0; x<1000; ++x)
	{
		for (int y=0; y<1000; ++y)
		{
			calculatePullForPoint(x, y);
		}
	}
}

void calculatePull(Move *m)
{
	long deltaX, deltaY;
	double pull;//, pull1 = 0.0, pull2 = 0.0;
	double pulls[20];
	int pCount;
	for (int x=0; x<1000; ++x)
	{
		for (int y=0; y<1000; ++y)
		{
			deltaX = m->x - x;
			deltaX = deltaX * deltaX;
			deltaY = m->y - y;
			deltaY = deltaY * deltaY;
			if (deltaX > 0 || deltaY > 0)
			{
				pull = 1.0 / (deltaX + deltaY);
			}
			else
			{
				pull = 1000000;	// infinity approximation
			}

			for (pCount=0; pCount < totalPlayers; ++pCount)
			{
				pulls[pCount] = matrices[pCount][x][y];
			}
			//pull1 = matrix1[x][y];
			//pull2 = matrix2[x][y];

			pulls[m->playerNum-1] += pull;
			/*if (currPlayer == 1)
			{
				 pull1 += pull;
			}
			else
			{
				pull2 += pull;
			}*/

			// calc best score
			double bestScore = 0.0;
			int bestPlayerIndex;
			for (pCount=0; pCount<totalPlayers; ++pCount)
			{
				if (pulls[pCount] > bestScore)
				{
					bestScore = pulls[pCount];
					bestPlayerIndex = pCount;
				}
			}
			playerScores[bestPlayerIndex] += 1;

			/*if (pull1 > pull2)
				player1Score += 1;
			else if (pull2 > pull1)
				player2Score += 1;*/
		}
	}
}

void runTestMoves()
{
	//int bestp1score = 0; int bestp2score = 0;
	
	char tmpstr[100];
	int pCount=0;
	for (int i=0; i<testMoves.size(); ++i)
	{
		//player1Score = 0;
		//player2Score = 0;
		// reset scores
		for (pCount=0; pCount<totalPlayers; ++pCount)
		{
			playerScores[pCount] = 0;
		}

		//moves[movesNum] = testMoves[i];	// this was already commented out
		calculatePull(testMoves[i]);
		if (!outputString.empty())
			outputString += ",";

		sprintf(tmpstr, "%d,%d", testMoves[i]->x, testMoves[i]->y);
		outputString += tmpstr;
		for (pCount=0; pCount<totalPlayers; ++pCount)
		{
			outputString += ",";
			sprintf(tmpstr, "%d", playerScores[pCount]);
			outputString += tmpstr;
		}

		//moves.pop_back();
	}
}

void initMatrix()
{
	int x, y;
	for (x=0; x<1000; ++x)
	{
		for (y=0; y<1000; ++y)
		{
			for (int pCount=0; pCount<totalPlayers; ++pCount)
			{
				matrices[pCount][x][y] = 0.0;
			}
			//matrix1[x][y] = 0.0;
			//matrix2[x][y] = 0.0;
		}
	}
}

void loadCalculatedValues()
{
	int x, y;
	std::ifstream input("matrix.txt");
	if (input)
	{
		for (x=0; x<1000; ++x)
		{
			for (y=0; y<1000; ++y)
			{
				//input >> matrix1[x][y] >> matrix2[x][y];
			}
		}
		input.close();
	}
	else
	{
		initMatrix();
	}

}

int main(int argc, char* argv[])
{
	//loadCalculatedValues();
	parseFile("input.txt");
	initMatrix();
	calculateCurrentMoves();
	runTestMoves();
	outputFile("output.txt");
	//std::cout << "p1 score is " << player1Score << " p2 score is " << player2Score << std::endl;
	return 0;
}

