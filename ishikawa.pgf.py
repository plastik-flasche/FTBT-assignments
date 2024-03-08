# Credit: https://github.com/JuGonz21/Fishbone

categories = {
    'Mensch': ['Fingerabdrücke', 'Ungeschultes Personal'],
    'Methode': ['Trocknungsdauer'],
    'Messung': [],
    'Material': ['Vorlage ist faltig', 'Tonerqualität schlecht', 'Papierdicke zu klein', 'Papiermaterial schlecht', 'Zu helle Farben'],
    'Maschine': ['Lampe zu halt', 'Glasfläche verschmutzt', 'Aufheizung des Gerät', 'Fördergummiräder verschmutzt'],
    'Milieu': ['Klimatisierung fehlt'],
    'Management': ['Walzenrolle nicht gewartet', 'Wartungsintervalle zu groß']
}


colors = [
    (0.18, 0.57, 0.89, 1),
    (0.88, 0.37, 0.6, 1),
    (0.11, 0.65, 0.11, 1),
    (0.98, 0.05, 0.05, 1),
    (0.2, 0.4, 0.6, 0.8),
    (0.8, 0.1, 0.5, 0.5),
    (0.5, 0.7, 0.3, 0.6),
    (0.9, 0.5, 0.2, 0.7),
    (0.6, 0.7, 0.3, 0.4),
    (0.6, 0.5, 0.2, 0.5)
]

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Wedge

import matplotlib
matplotlib.use("pgf")

def fishbone_chart (rgba_colors):
    # Create the fishbone diagram

    if len(rgba_colors) <= 6:  # Si la longitud es menor o igual a 6
        fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
    elif len(rgba_colors) <= 8:  # Si la longitud es mayor a 6
        fig, ax = plt.subplots(figsize=(15, 9), constrained_layout=True)
        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
    else:
        fig, ax = plt.subplots(figsize=(21, 12), constrained_layout=True)
        ax.set_xlim(-8.5, 8.5)
        ax.set_ylim(-8.5, 8.5)

    ax.axis('off')

    print (rgba_colors)
    face_colors = []
    for rgba in rgba_colors:
        rgba_values = [int(val) if i < 3 else val for i, val in enumerate(rgba)]
        # Multiply the first three values (RGB) by 255 and leave the alpha value intact
        face_colors.append(tuple(rgba_values))



    def problems(data: str,
                 problem_x: float, problem_y: float,
                 prob_angle_x: float, prob_angle_y: float,
                 face_color):  # Agregar un nuevo parámetro para el color
        """
        Draw each problem section of the Ishikawa plot.
        """

        #print (face_color)
        ax.annotate(str.upper(data), xy=(problem_x, problem_y),
                    xytext=(prob_angle_x, prob_angle_y),
                    fontsize='10',
                    color='white',
                    weight='bold',
                    xycoords='data',
                    verticalalignment='center',
                    horizontalalignment='center',
                    textcoords='offset fontsize',
                    arrowprops=dict(arrowstyle="->", facecolor='black'),
                    bbox=dict(boxstyle='square',
                              facecolor= face_color,  # Usar el color pasado como argumento
                              pad=1.2))


    def causes(data: list, cause_x: float, cause_y: float,
               cause_xytext=(-9, -0.3), top: bool = True):
        """
        Place each cause to a position relative to the problems
        annotations.

        Parameters
        ----------
        data : indexable object
            The input data. IndexError is
            raised if more than six arguments are passed.
        cause_x, cause_y : float
            The `X` and `Y` position of the cause annotations.
        cause_xytext : tuple, optional
            Adjust to set the distance of the cause text from the problem
            arrow in fontsize units.
        top : bool

        Returns
        -------
        None.

        """
        for index, cause in enumerate(data):
            # First cause annotation is placed in the middle of the problems arrow
            # and each subsequent cause is plotted above or below it in succession.

            # [<x pos>, [<y pos top>, <y pos bottom>]]
            coords = [[0, [0, 0]],
                      [0.23, [0.5, -0.5]],
                      [-0.46, [-1, 1]],
                      [0.69, [1.5, -1.5]],
                      [-0.92, [-2, 2]],
                      [1.15, [2.5, -2.5]]]
            if top:
                cause_y += coords[index][1][0]
            else:
                cause_y += coords[index][1][1]
            cause_x -= coords[index][0]

            ax.annotate(cause, xy=(cause_x, cause_y),
                        horizontalalignment='center',
                        xytext=cause_xytext,
                        fontsize='9',
                        xycoords='data',
                        textcoords='offset fontsize',
                        arrowprops=dict(arrowstyle="->",
                                        facecolor='black'))


    def draw_body(data: dict, face_colors: list):
        """
        Place each section in its correct place by changing
        the coordinates on each loop.

        Parameters
        ----------
        data : dict
            The input data (can be list or tuple). ValueError is
            raised if more than six arguments are passed.

        Returns
        -------
        None.

        """
        second_sections = []
        third_sections = []
        fourth_sections = []
        fifth_sections = []
        # Resize diagram to automatically scale in response to the number
        # of problems in the input data.
        if len(data) == 1 or len(data) == 2:
            spine_length = (-2.1, 2)
            head_pos = (2, 0)
            tail_pos = ((-2.8, 0.8), (-2.8, -0.8), (-2.0, -0.01))
            first_section = [1.6, 0.8]
        elif len(data) == 3 or len(data) == 4:
            spine_length = (-3.1, 3)
            head_pos = (3, 0)
            tail_pos = ((-3.8, 0.8), (-3.8, -0.8), (-3.0, -0.01))
            first_section = [2.6, 1.8]
            second_sections = [-0.4, -1.2]
        elif len(data) == 5 or len(data) == 6:
            spine_length = (-4.1, 4)
            head_pos = (4, 0)
            tail_pos = ((-4.8, 0.8), (-4.8, -0.8), (-4.0, -0.01))
            first_section = [3.5, 2.7]
            second_sections = [1, 0.2]
            third_sections = [-1.5, -2.3]
        elif len(data) == 7 or len(data) == 8:
            spine_length = (-5.1, 5)
            head_pos = (5, 0)
            tail_pos = ((-5.8, 0.8), (-5.8, -0.8), (-5.0, -0.01))
            first_section = [4.4, 3.65] #+0.8
            second_sections = [2, 1.25]  #+1.4   Posicion de las Labels generales y despues las flechas y causas
            third_sections = [-0.4, -1.2]  #+1.2
            forth_sections = [-2.6, -3.4]
        elif len(data) == 9 or len(data) == 10 :
            spine_length = (-6.1, 6)
            head_pos = (6, 0)
            tail_pos = ((-6.8, 0.8), (-6.8, -0.8), (-6.0, -0.01))
            first_section = [5.4, 4.7] #+0.8
            second_sections = [3, 2.3]  #+1.4   Posicion de las Labels generales y despues las flechas y causas
            third_sections = [0.6, -0.1]  #+1.2
            forth_sections = [-1.6, -2.45]
            fifth_sections = [-3.4, -4.45]
        else:
            pass


        # Change the coordinates of the annotations on each loop.
        for index, problem in enumerate(data.values()):
            top_row = True
            cause_arrow_y = 1.7
            if index % 2 != 0:  # Plot problems below the spine.
                top_row = False
                y_prob_angle = -16
                cause_arrow_y = -1.7
            else:  # Plot problems above the spine.
                y_prob_angle = 16
            # Plot the 3 sections in pairs along the main spine.
            if index in (0, 1):
                prob_arrow_x = first_section[0]
                cause_arrow_x = first_section[1]
            elif index in (2, 3):
                prob_arrow_x = second_sections[0]
                cause_arrow_x = second_sections[1]
            elif index in (4,5):
                prob_arrow_x = third_sections[0]
                cause_arrow_x = third_sections[1]
            elif index in (6,7):
                prob_arrow_x = forth_sections[0]
                cause_arrow_x = forth_sections[1]
            else:
                prob_arrow_x = fifth_sections[0]
                cause_arrow_x = fifth_sections[1]
            if index > 9:
                raise ValueError(f'Maximum number of problems is 8, you have entered '
                                 f'{len(data)}')


            # draw main spine
            ax.plot(spine_length, [0, 0], color='tab:grey', linewidth=3.5)
            # draw fish head
            ax.text(head_pos[0] + 0.1, head_pos[1] - 0.05, 'Schlechte Kopien', fontsize=10,
                    weight='bold', color='white')

            semicircle = Wedge(head_pos, 1.5, 270, 90, fc='tab:grey')
            semicircle.set_fill(True)
            ax.add_patch(semicircle)
            # draw fishtail
            triangle = Polygon(tail_pos, fc='tab:grey')
            ax.add_patch(triangle)

            print (data)
            # Pass each category name to the problems function as a string on each loop.
            problems(list(data.keys())[index], prob_arrow_x, 0, -12, y_prob_angle, face_colors[index])
            # Start the cause function with the first annotation being plotted at
            # the cause_arrow_x, cause_arrow_y coordinates.
            causes(problem, cause_arrow_x, cause_arrow_y, top=top_row)


    fishbone_cat = categories

    # print(categories)

    #print(categories)

    draw_body(fishbone_cat, colors)
    plt.savefig("ishikawa.pgf")

fishbone_chart(colors)