#!/bin/bash

# =======================
# @Author: Liu Yuchen
# @Date  : 2023-05-02
#
# =======================

MODULE="ml-toy"
VERSION=$(grep "__version__" "${MODULE}/__init__.py" \
  | awk -F '=' '{print $2}' | sed 's/[ |"]//g')
echo "The Version is: ${VERSION}"

skipTest=false

function usage() {
  echo "Usage:"
  echo "  sh build.sh [option] "
  echo "    -h|--help       # 帮助信息"
  echo "    --skipTest      # 跳过测试: true/false. 默认 false"
  echo "Example:"
  echo "  sh build.sh --skipTest=true"
}

function param_parser() {
  unset OPTIND
  while getopts t:e:-:h opt
  do
    case "${opt}" in
      h) usage ; exit 0 ;;
      -)
        case ${OPTARG} in
          help) usage ; exit 0 ;;
          skipTest=*) skipTest=${OPTARG#*=} ;;
        esac
        ;;
      *) echo "Please input -h | --help get help."
        exit 1 ;;
    esac
  done
}

function clean() {
	if [[ -f "./build/lib/${MODULE}-${VERSION}.zip" ]]; then
		rm -r "./build/lib/${MODULE}-${VERSION}.zip"
	fi

	if [[ -d "./build/lib/${MODULE}" ]]; then
		rm -r "./build/lib/${MODULE}"
	fi
}

function test_case() {
  if [[ "${skipTest}" == "true" ]]; then
		echo "Skip test......"
	else
		pytest
	fi
}

function build_python_package() {
  python ./setup.py build
	python ./setup.py sdist
	python ./setup.py bdist_wheel
}

function build_pyspark_package() {
  # 构建 PySpark 能够使用的 config hub
	cd ./build/lib/
	zip -r "${MODULE}-${VERSION}.zip" "${MODULE}/"
}

function main() {
  param_parser "$@"
  clean
	test_case
	build_python_package
	build_pyspark_package
}

main "$@"
