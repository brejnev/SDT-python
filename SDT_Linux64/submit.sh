#PBS -q UCTlong
#PBS -l nodes=1:series400M:ppn=1
#PBS -N SDT_Linux64
#PBS -e /home/brejnev/SDT_project/SDT_project_uplaod/SDT_Linux64/SDT_Linux64.err
#PBS -o /home/brejnev/SDT_project/SDT_project_uplaod/SDT_Linux64/SDT_Linux64.out

cd /home/brejnev/SDT_project/SDT_project_uplaod/SDT_Linux64

python SDT_Linux64.py test.fas muscle


