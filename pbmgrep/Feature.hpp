#define MAX_WIDTH 1600
#define COLS32 MAX_WIDTH / 32


class Feature
{
public:
  char* filename;
  int cols;
  int rows;
  int cols32;
  unsigned int right_mask;
  unsigned int* integers;
  Feature(const char* _filename);
  ~Feature();
  unsigned int getBottomLeft();
  bool match(unsigned int input[][32][COLS32], int cycle_rows,
	     int offset, int column, int y);
};
