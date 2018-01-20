#!/usr/bin/env bash

FLAG_FORCE=1  # 1 or 0
PIZZA=1 # install pizza (LAMMPS python analysis module)

function install_pizza {
  if [[ ! -f pizza.tar.gz ]]; then
    echo "Download pizza.tar.gz from http://pizza.sandia.gov/index.html"
    return
  fi
  [[ -d pizza ]] && rm -rf pizza
  mkdir -p pizza
  echo "Extract pizza.tar.gz"
  tar -xf pizza.tar.gz  -C pizza --strip-components=2 pizza-9Oct15/src # POSSIBLE ERROR
  FILES=$(ls pizza)
cat<<EOF > pizza/__init__.py
#!/usr/bin/env python
"""
LAMMPS PIZZA.py from from http://pizza.sandia.gov/index.html
only the src files
"""

EOF
  for file in ${FILES}; do
    module=${file%.py}
    case $module in
      animate|gl|image) ;;
      *)
      echo "import $module" >> pizza/__init__.py
      ;;
    esac
  done

  if ! grep -Fq 'import pizza' __init__.py; then
    echo -e "\nimport pizza\n" >> __init__.py
  fi
}

if [[ ! -f __init__.py ]]; then
cat<<EOF > __init__.py
#!/usr/bin/env python
"""External Libraries"""

EOF
fi


if [[ "$PIZZA" == "1" ]]; then
    if [[ "$FLAG_FORCE" == "1" ]]; then
        install_pizza
    fi
fi

