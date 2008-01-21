#include <list>
#include "Feature.hpp"

extern "C" {
#include <pbm.h>
}


void read_integers(bit* input, int offset, unsigned int* integers, int cols32)
{
  int x = offset;
  unsigned int i;
  for (int col = 0; col < cols32; col++) {
    i = 0;
    for (int b = 0; b < 32; b++) {
      i = i << 1;
      if (input[x]) i++;
      x++;
    }
    integers[col] = i;
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
  const int cols32 = cols / 32;
  if (cols > MAX_WIDTH) {
    fprintf(stderr, "image is too wide (%d > %d pixels)\n", cols, MAX_WIDTH);
    exit(2);
  }
  unsigned int integers[cycle_rows][32][COLS32];
  bit* input = pbm_allocrow(cols);

  for (int y = 0; y < rows; y++) {
    // fprintf(stderr, "%d\r", y);
    pbm_readpbmrow(stdin, input, cols, format);
    for (int offset = 0; offset < 32; offset++) {
      read_integers(input, offset, integers[y % cycle_rows][offset], cols32);
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
	    }
	  }
	}
      }
    }
  }
  pbm_freerow(input);
}
