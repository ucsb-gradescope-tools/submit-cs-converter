if [ "$#" -eq 2 ]; then
	if [ "${1:0:1}" = "/" ]; then
		ZIP_FILE=$1
	else
		ZIP_FILE=`pwd`/$1
	fi

	if [ "${2:0:1}" = "/" ]; then
		OUTDIR=$2
	else
		OUTDIR=`pwd`/$2
	fi
else
	echo "Usage: ./convert.sh assignment.zip outdir"
	exit 1
fi

if [ -d $2 ]; then
	echo "Error: output directory already exists"
	exit 1
fi

CONVERTER_DIR=`pwd`

mkdir $OUTDIR
cd $OUTDIR

mkdir REFERENCE-SOLUTION
mkdir EXECUTION-FILES
mkdir BUILD-FILES

# Pull necessary files from sample diff repo
git clone https://github.com/ucsb-gradescope-tools/sample-cpp-diff-autograder.git
cd sample-cpp-diff-autograder
git checkout factor-out-expected
# In case the repo was already cloned
git pull origin factor-out-expected
cd ..
cp sample-cpp-diff-autograder/MAKE-REFERENCE.sh .
cp sample-cpp-diff-autograder/grade.sh .
cp sample-cpp-diff-autograder/apt-get.sh .
rm -rf sample-cpp-diff-autograder/

python3 $CONVERTER_DIR/create-diffs-sh.py $ZIP_FILE

python3 $CONVERTER_DIR/move-assignment-files.py $ZIP_FILE

mv EXECUTION-FILES/execution_files/* EXECUTION-FILES
rm -rf EXECUTION-FILES/execution_files/

python3 $CONVERTER_DIR/create-expected-sh.py $ZIP_FILE