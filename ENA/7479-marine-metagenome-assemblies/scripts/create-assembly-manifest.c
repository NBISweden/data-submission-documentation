#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<malloc.h>
#include<alloca.h>
#include<ctype.h>

int nrCols = 0;
int nrRows = 0;
char tsvMatrix[3000][40][400];

void count(FILE *fin)
{
  char line[10000];
  int i = 0, j = 0, k = 0;

  fgets(line,10000,fin);
  while (line[k]!='\0')
    {
        while (line[k]!='\t' && line[k]!='\0' && line[k]!='\n' && line[k]!='\r')
            k++;
        if (line[k]!='\0')
        {
            k++;
            j++;
        }
    }
  while (!feof(fin))
    {
      i++;
      fgets(line,10000,fin);
    }
  rewind(fin);
  nrRows = i+1;
  nrCols = j-1;
  /*printf("There are %i rows and %i columns.\n",nrRows, nrCols);*/
  if (nrRows>3000 || nrCols>40)
  {
    fprintf(stderr,"The prg  cannot scale, either number of rows (%i) > 3000 or columns (%i) > 40, will exit\n",nrRows, nrCols);
    exit(0);
  }
}
int readMetaRecord(char *line, char *post, int start)
{
  int i, j;
  i = start;
  j = 0;

  while(line[i]!='\t' && line[i]!='\0' && line[i]!='\n' && line[i]!='\r' && line[i]!=';')
    {
      post[j] = line[i];
      j++;
      i++;
    }
  post[j] = '\0';
  if (line[i]=='\t' || line[i]==';')
    i++;
  return(i);
}
void readRows(FILE *fin) 
{
  char line[10000];
  int i, j, k;

  for (j=0;j<nrRows;j++)
  {
    fgets(line,10000,fin); 
    i = 0;
    for (k=0;k<nrCols;k++)
    {
      i = readMetaRecord(line,tsvMatrix[j][k],i);
      /*printf("Read %s\n",tsvMatrix[j][k]);*/
    }
  }
}

void printMatrix()
{
    int i, j;
    for (i=0;i<nrRows;i++)
    {
        for (j=0;j<nrCols;j++)
        {
            printf("%s;",tsvMatrix[i][j]);
        }
        printf("\n");
    }
}
void createFileName(char *initName, char *name)
{
    int i; 

    i = 0;
    while (initName[i]!='\t' && initName[i]!='\0')
    {
        name[i] = initName[i];
        i++;
    }
    name[i] = '\0';
    strcat(name,"-manifest.txt");
    printf("java -jar ../../webin-cli-7.0.1.jar -context genome -ascp -userName $1 -password '$2' -manifest %s -$3\n",name);
}

int main(argc,argv)
int argc;
char **argv;
{
  FILE *finTsv, *fout;
  int i, j, nameCol;
  char outFile[100];

  if (argc < 3)
    {
      printf("The prg wants a tsv file with header row formatted and ordered as the field names in the output manifest (e.g. STUDY), and the column number to use as basis for creating the output file name (e.g. the ASSEMBLY_NAME column) (count from 0)\n");
    }
  else
    {
      if (!(finTsv=fopen(argv[1],"r")))
      {
        fprintf(stderr,"Can't open file %s \n",argv[1]);
        exit(0);
      }
      else 
      {
          /* Read the metadata file */

          count(finTsv);
          readRows(finTsv);
          /* printMatrix(); */
          fclose(finTsv);
          nameCol = atoi(argv[2]);
          /* printf("Will use column (number %i) %s as base for output file names\n",nameCol, tsvMatrix[0][nameCol]); */
          /* For all rows exept header row */
          for (i=1; i<nrRows; i++) 
          {
            /* Create manifest file */
            createFileName(tsvMatrix[i][nameCol],outFile);
            if (!(fout=fopen(outFile,"w")))
            {
                fprintf(stderr,"Can't open file %s \n",outFile);
                exit(0);
            }
            else
            {
                for (j=0; j<nrCols; j++)
                    fprintf(fout,"%s: %s\n",tsvMatrix[0][j],tsvMatrix[i][j]);
                fclose(fout);
            }
          }
      }
    }
}
