import os
from operator import itemgetter
import numpy as np
import pandas as pd


# load mentores answers
mentores_answers = pd.read_csv('data/mentores/Registo mentores.csv')

# load mentorandos answers
mentorandos_answers = pd.read_csv('data/mentorandos/Registo mentorandos.csv')


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


def check_qualities(mentor_qualities, mentorando_qualities):
    """
    Checks qualities `mentorando` is looking for in `mentor` and finds
    similarities in qualities `mentor` has.

    Parameters:
    - mentor_qualities (str): mentor qualities
    - mentorando_qualities (str): qualities mentorando looks for on a mentor.

    Returns:
    - freq_commonalities (int): frequency of common qualities found.
    """
    mentor_qualities_list =  mentor_qualities.split(";")
    mentorando_qualities_list = mentorando_qualities.split(";")
    commonalities = list(set(mentor_qualities_list).intersection(mentorando_qualities_list))
    return len(commonalities)


def check_cinema_genders(mentor_favorite_genders, mentorando_favorite_genders):
    """
    Check for commonalities in mentor and mentorando's favorite movie/series genders.

    Parameters:
    - mentor_favorite_genders (str): mentor favorite genders
    - mentorando_favorite_genders (str): mentorando favorite genders.

    Returns:
    - freq_commonalities (int): frequency of common favorite genders found.
    """
    mentor_favorite_genders_list =  mentor_favorite_genders.split(";")
    mentorando_favorite_genders_list = mentorando_favorite_genders.split(";")
    commonalities = list(set(mentor_favorite_genders_list).intersection(mentorando_favorite_genders_list))
    return len(commonalities)


def check_personalities(mentor_personality, mentorando_personality):
    """
    Computes a personality similarity index between mentor and mentorando.

    Parameters:
    - mentor_personality (numpy.array): mentor personality scores
    - mentorando_personality (numpy.array): mentorando personality scores.

    Returns:
    - personality_similarity (int): personality similarity score, from 0 to 1,
    where 0 is less similar and 1 is more similar.
    """
    # Euclidean distance
    personality_similarity = np.linalg.norm(mentor_personality-mentorando_personality)
    return personality_similarity


def check_hobbies(mentor_hobbies, mentorando_hobbies):
    """
    Computes a similarity index between mentor and mentorando's hobbies.

    Parameters:
    - mentor_hobbies (numpy.array): mentor's hobbies
    - mentorando_hobbies (numpy.array): mentorando's hobbies.

    Returns:
    - hobbies_similarity (int): hobbies similarity score, from 0 to 1,
    where 0 is less similar and 1 is more similar.
    """
    # Euclidean distance
    hobbies_similarity = np.linalg.norm(mentor_hobbies-mentorando_hobbies)
    return hobbies_similarity


def similarity_score(mentor, mentorando):
    """
    Similarity score between a `mentor` and a `mentorando`
    """

    is_same_entry = check_entry(
        mentor['Indique de que modo ingressou na FCUL, selecionando uma (ou mais) das opções abaixo.'],
        mentorando['Indique as suas condições de entrada na faculdade, selecionando uma (ou mais) das opções abaixo:']
    )

    common_qualities_count = check_qualities(
        mentor['Selecione até 3 qualidades que melhor o caracterizem como mentor.'],
        mentorando['Selecione até 3 qualidades de um bom mentor:']
    )

    common_cinema_genders = check_cinema_genders(
        mentor['Selecione até 3 dos seus géneros de filmes/séries favoritos:'],
        mentorando['Selecione até 3 dos seus géneros de filmes/séries favoritos:']
    )

    hobbies_similarity = check_hobbies(
        mentor[11:20],
        mentorando[15:24]
    )

    personality_similarity = check_personalities(
        mentor.to_numpy()[20:],
        mentorando.to_numpy()[24:]
    )

    s_a = ( (10/7)*int(is_same_entry) + (3/10)*common_qualities_count + (2/10)*common_cinema_genders ) / ( 10+3+2 )
    s_b = (2/hobbies_similarity) + (1/personality_similarity)

    score = s_a + s_b

    return score


mentorandos_best_fits = [] # stores mentorandos' best mentor candidates

for mentorando_idx in mentorandos_answers.index:
    mentorando = mentorandos_answers.loc[mentorando_idx]

    mentorando_pair_scores = [] # stores similarity scores with available mentors

    for mentor_idx in mentores_answers.index:
        mentor = mentores_answers.loc[mentor_idx]

        mentor_curso = mentor['Qual o curso em que está inscrito no presente ano letivo?']
        mentorando_curso = mentor['Qual o curso em que está inscrito no presente ano letivo?']

        if mentor_curso == mentorando_curso:

            mentor_age = mentor['Idade (no início do presente ano letivo)']
            mentorando_age = mentorando['Idade (no início do presente ano letivo)']

            if mentor_age >= mentorando_age:
                s_score = similarity_score(mentor=mentor, mentorando=mentorando)
                mentorando_pair_scores.append( (mentores_answers.loc[mentor_idx, 'Nome completo'], s_score) )

    # sort mentors by descending order of similarity scores
    mentorando_pair_scores_sorted = sorted(mentorando_pair_scores, key=itemgetter(1), reverse=True)
    mentorandos_best_fits.append([mentorando['Nome completo'], ";".join([mentorando_pair[0] for mentorando_pair in mentorando_pair_scores_sorted[:3]])])

mentorandos_best_fits_df = pd.DataFrame(mentorandos_best_fits, columns=['Nome completo', 'TOP 3 candidatos a mentor'])
mentorandos_best_fits_df.set_index('Nome completo', inplace=True)

if not os.path.exists('results'):
    os.makedirs('results')
mentorandos_best_fits_df.to_csv('./results/mentorandos-best-fits.csv')
