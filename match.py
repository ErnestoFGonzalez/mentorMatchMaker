import numpy as np
import pandas as pd


# load mentores answers
mentores_answers = pd.read_csv('data/mentores/Registo mentores.csv')

# load mentorandos answers
mentorandos_answers = pd.read_csv('data/mentorandos/Registo mentorandos.csv')


def similarity_score(mentor, mentorando):
    """
    Similarity score between a `mentor` and a `mentorando`
    """

    # select quantifiable columns
    mentor_coords = mentor[11:]
    mentorando_coords = mentorando[15:]

    # Euclidean distance
    dist = np.linalg.norm(mentor_coords-mentorando_coords)

    return dist


for mentor_idx in mentores_answers.index:
    mentor = mentores_answers.loc[mentor_idx].to_numpy()
    for mentorando_idx in mentorandos_answers.index:
        mentorando = mentorandos_answers.loc[mentorando_idx].to_numpy()
        s_score = similarity_score(mentor=mentor, mentorando=mentorando)
        print('{} and {} have a {:.2f} dissimilarity score.'.format(
            mentores_answers.loc[mentor_idx, 'Nome completo'],
            mentorandos_answers.loc[mentorando_idx, 'Nome completo'],
            s_score))
