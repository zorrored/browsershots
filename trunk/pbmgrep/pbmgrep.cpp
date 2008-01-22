#include <list>
#include "Feature.hpp"

extern "C" {
#include <pbm.h>
}


void read_integers(bit* input, unsigned int integers[32][COLS32], int cols)
{
  unsigned int i = 0;
  for (int x = 0; x < 31; x++) {
    i = i << 1;
    if (input[x]) i++;
  }
  int offset = 0;
  int col = 0;
  for (int x = 31; x < cols; x++) {
    i = i << 1;
    if (input[x]) i++;
    integers[offset][col] = i;
    if (offset < 31) {
      offset++;
    } else {
      offset = 0;
      col++;
    }
  }
}


int main(int argc, char* argv[])
{
  pbm_init(&argc, argv);
  if (argc < 2) {
    fprintf(stderr, "usage: pbmgrep <feature.pbm> ...\n");
    return 1;
  }
  std::list<Feature*> features;
  int cycle_rows = 0;
  for (int i = 1; i < argc; i++) {
    features.push_back(new Feature(argv[i]));
    cycle_rows = max(cycle_rows, features.back()->rows);
  }
  // fprintf(stderr, "features %d\n", features.size());
  // fprintf(stderr, "cycle_rows %d \n", cycle_rows);

  int cols;
  int rows;
  int format;
  pbm_readpbminit(stdin, &cols, &rows, &format);
  if (cols > MAX_WIDTH) {
    fprintf(stderr, "image is too wide (%d > %d pixels)\n", cols, MAX_WIDTH);
    return 2;
  }
  const int cols32 = cols / 32;
  unsigned int integers[cycle_rows][32][COLS32];
  bit* input = pbm_allocrow(cols);

  for (int y = 0; y < rows; y++) {
    // fprintf(stderr, "%d\r", y);
    pbm_readpbmrow(stdin, input, cols, format);
    read_integers(input, integers[y % cycle_rows], cols);
    for (int offset = 0; offset < 32; offset++) {
      std::list<Feature*>::iterator iter;
      for (iter = features.begin(); iter != features.end(); iter++) {
	Feature* feature = (*iter);
	if (y >= feature->rows - 1) {
	  for (int column = 0; column < cols32 - feature->cols32; column++) {
	    if (feature->match(integers, cycle_rows, offset, column, y)) {
	      fprintf(stdout, "%d\t%d\t%d\t%d\t%s\n",
		      offset + column * 32, y - feature->rows + 1,
		      feature->cols, feature->rows,
		      feature->filename);
	      return 1;
	    }
	  }
	}
      }
    }
  }
  pbm_freerow(input);
  return 0;
}
