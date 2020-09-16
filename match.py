import re
import numpy as np
import pandas as pd


# load mentores answers
mentores_answers = pd.read_csv('data/mentores/Registo mentores.csv')

# load mentorandos answers
mentorandos_answers = pd.read_csv('data/mentorandos/Registo mentorandos.csv')


# for column in mentorandos_answers.columns:
#     print(column)

mentor_qualities = mentores_answers['Selecione até 3 qualidades que melhor o caracterizem como mentor.']
print(mentor_qualities)


def check_entry(mentor_entry, mentorando_entry):
    """
    Checks `mentor` and `mentorando` entry mechanism to FCUL.

    Parameters:
    - mentor_entry (str): mentor questionnaire answers
    - mentorando_entry (str): mentorando questionnaire answers

    Returns:
    - is_same_entry (bool): Indicates if mentor and mentorando entered FCUL by
    same mechanism.
    """
    is_same_entry = mentor_entry == mentorando_entry
    return is_same_entry


def check_personality(mentor_qualities, mentorando_qualities):
    """
    Checks qualities `mentorando` is looking for in `mentor` and finds
    similarities in qualities `mentor` has.

    Parameters:
    - mentor_qualities (str): mentor qualities
    - mentorando_qualities (str): qualities mentorando looks for on a mentor.

    Returns:
    - freq_commonalities (int): frequency of common qualities found.
    """
    pass


# for mentor_idx in mentores_answers.index:
#     mentor = mentores_answers.loc[mentor_idx].to_numpy()
#     for mentorando_idx in mentorandos_answers.index:
#         mentorando = mentorandos_answers.loc[mentorando_idx].to_numpy()
#         print('{} and {} have same entry: {}'.format(
#         mentores_answers.loc[mentor_idx, 'Nome completo'],
#         mentorandos_answers.loc[mentorando_idx, 'Nome completo'],
#         check_entry(
#             mentores_answers.loc[mentor_idx, 'Indique de que modo ingressou na FCUL, selecionando uma (ou mais) das opções abaixo.'],
#             mentorandos_answers.loc[mentorando_idx, 'Indique as suas condições de entrada na faculdade, selecionando uma (ou mais) das opções abaixo:'])))

# def similarity_score(mentor, mentorando):
#     """
#     Similarity score between a `mentor` and a `mentorando`
#     """
#
#     # select quantifiable columns
#     mentor_coords = mentor[11:]
#     mentorando_coords = mentorando[15:]
#
#     # Euclidean distance
#     dist = np.linalg.norm(mentor_coords-mentorando_coords)
#
#     return dist
#
#
# for mentor_idx in mentores_answers.index:
#     mentor = mentores_answers.loc[mentor_idx].to_numpy()
#     for mentorando_idx in mentorandos_answers.index:
#         mentorando = mentorandos_answers.loc[mentorando_idx].to_numpy()
#         # discard mentorando older than mentor
#         # se veio de outro curso flag user
#         # se não é portugês flag user
#         s_score = similarity_score(mentor=mentor, mentorando=mentorando)
#         print('{} and {} have a {:.2f} dissimilarity score.'.format(
#             mentores_answers.loc[mentor_idx, 'Nome completo'],
#             mentorandos_answers.loc[mentorando_idx, 'Nome completo'],
#             s_score))
