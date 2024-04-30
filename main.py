from manim import *
import itertools
from math import comb, factorial

from rich.console import HighlighterType

def flatten(xss):
    return [x for xs in xss for x in xs]

def eulerian(n, k):

    return sum([(-1)**i * comb(n + 1, i) * (k + 1 - i)**n for i in range(k + 1)])


class IntroSequence(Scene):

    def construct(self):

        title = Tex("Eulerian Numbers", font_size=96)

        line = Line(start=ORIGIN, end=[10, 0, 0])

        author = Tex("plasmaofthedawn")

        Group(title, line, author).arrange(DOWN * 2)
        
        self.play(
            AnimationGroup(Write(title), Create(line), Write(author), lag_ratio=0.1)
        )

        self.wait(1)

        self.play(
            Unwrite(title, reverse=False), Uncreate(line), Unwrite(author, reverse=False)
        )


class IntroEulerian(Scene):
    
    
    def construct(self):
        
        title = MathTex(r"A(", "n", ", ", "k", ")", "=", color=TEAL).scale(1.5)
        title.set_color_by_tex_to_color_map({
            "n": YELLOW,
            "k": PURPLE,
            "=": WHITE
        })

        definition1 = Tex("The number of permutations")
        definition2 = Tex("of the numbers $1$ to ", "$n$", " with ", "$k$",  " ascents.")

        definition2.set_color_by_tex_to_color_map({
            "$n$": YELLOW,
            "$k$": PURPLE
        })

        def_group = VGroup(definition1, definition2).arrange(DOWN)

        Group(title, def_group).arrange(DOWN * 2)

        self.play(Write(title))
        self.play(Write(def_group))

        self.wait(1)

        self.play(Unwrite(title), Uncreate(def_group))


        

class DemonstrateDefinition(Scene):

    def construct(self):       

        sequence_length = MathTex(r"n", r"=", "3")
        sequence_length.set_color_by_tex("n", YELLOW)
        end_sequence_length = sequence_length.copy().move_to(LEFT * 2.5 + UP * 3)

        self.play(
            Write(sequence_length)
        )

        self.play(
            Transform(sequence_length, end_sequence_length)
        )

        top_one = MathTex(r"1")
        top_two = MathTex(r"2")
        top_three = MathTex(r"3")

        top = Group(top_one, top_two, top_three).arrange(RIGHT)

        top.move_to(ORIGIN + 3 * UP)

        self.play(
            *[Create(x) for x in top]
        )

        perm_groups = []
        numbers = [[], [], []]

        up_arrow = Arrow(start=ORIGIN, end=[.5, .8, 0], stroke_width=2, color=GREEN)
        down_arrow = Arrow(start=ORIGIN, end=[.5, -.8, 0], stroke_width=2, color=RED)

        arrows = []
        up_arrows = []

        ascent_counts = []

        for permutation in itertools.permutations([1, 2, 3]):
            
            this_group = []

            last = None

            arrows.append([])
            up_arrows.append([])

            ascents = 0
            
            for i in permutation:
                obj = MathTex(str(i))

                if last != None:

                    if last < i:
                        arr = up_arrow.copy()
                        up_arrows[-1].append(arr)
                        ascents += 1
                    else:
                        arr = down_arrow.copy()

                    this_group.append(arr)
                    arrows[-1].append(arr)

                this_group.append(obj)
                numbers[i-1].append(obj)

                last = i


            ascent_counts.append(
                MathTex(str(ascents), color=PURPLE) #, Tex("ascent" if ascents == 1 else "ascents")).arrange(RIGHT * 0.6))
            )

            perm_groups.append(Group(*this_group).arrange(RIGHT * 0.8))

        perm_group = Group(*perm_groups).arrange(DOWN).move_to(ORIGIN)
        count_group = Group(*ascent_counts).arrange(DOWN, center=False).move_to(ORIGIN + RIGHT * 2)


        # Create sequences
        self.play(
            AnimationGroup(
                AnimationGroup(*[ReplacementTransform(top_one.copy(), x) for x in numbers[0]], lag_ratio=0.15),
                AnimationGroup(*[ReplacementTransform(top_two.copy(), x) for x in numbers[1]], lag_ratio=0.15),
                AnimationGroup(*[ReplacementTransform(top_three.copy(), x) for x in numbers[2]], lag_ratio=0.15),
                lag_ratio=0.25
            )
        )

        # highlight 2, 1, 3

        target_perm = perm_group[2]

        self.play(
            FadeOut(top),
            Circumscribe(target_perm)
        )

        framebox1 = SurroundingRectangle(Group(target_perm[0], target_perm[2]))
        framebox2 = SurroundingRectangle(Group(target_perm[2], target_perm[4]))

        self.play(
            Create(framebox1)
        )

        greater_than = MathTex(">").move_to(target_perm[1])
        less_than = MathTex("<").move_to(target_perm[3])

        # show descent
        self.play(
            Write(greater_than)
        )
        self.play(
            ReplacementTransform(greater_than, target_perm[1])
        )

        # move box
        self.play(
            ReplacementTransform(framebox1, framebox2)
        )

        # show ascent
        self.play(
            Write(less_than)
        )
        self.play(
            ReplacementTransform(less_than, target_perm[3])
        )

        # remove box
        self.play(
            Uncreate(framebox2)
        )


        # add in the rest of the arrows
        self.play(
            AnimationGroup(
                *[x for x in [AnimationGroup(*[Create(x) for x in y if x not in target_perm]) for y in arrows if len([x for x in y if x not in target_perm]) > 0]],
            lag_ratio = 0.1)
        )


        ascent_title = Tex(r"\# of ascents").scale(0.7)
        ascent_line = Line(ORIGIN, LEFT*2)

        Group(ascent_title, ascent_line).arrange(DOWN).move_to(ORIGIN + RIGHT * 2 + UP * 2.5)

        # move perm group over and create title.
        self.play(
            perm_group.animate.move_to(perm_group.get_center() + LEFT * 2.5),
            Write(ascent_title), Create(ascent_line)
        )
        
        # highlight arrows - might be too much
        self.play(
            *[Circumscribe(x) for x in flatten(up_arrows)]
        )


        # add count group
        self.play(
            #AnimationGroup(
                #perm_group.animate.move_to(perm_group.get_center() + LEFT * 2.5),
                AnimationGroup(
                  *[AnimationGroup(*[ReplacementTransform(v.copy(), n) for v in x]) if len(x) != 0 else FadeIn(n) for x, n in zip(up_arrows, count_group)]
                , lag_ratio=0.1),
            #lag_ratio = 0.5)
        )

        brace_2 = Brace(count_group[0], direction=LEFT)
        total_2 = Tex(r"Total: ", "1")
        total_2[1].set_color(BLUE)
        brace_2.put_at_tip(total_2)
        
        brace_1 = Brace(Group(*count_group[1:5]), direction=LEFT)
        total_1 = Tex(r"Total: ", "4")
        total_1[1].set_color(BLUE)
        brace_1.put_at_tip(total_1)
        
        brace_0 = Brace(count_group[5], direction=LEFT)
        total_0 = Tex(r"Total: ", "1")
        total_0[1].set_color(BLUE)
        brace_0.put_at_tip(total_0)

        # get rid of the extra stuff and add braces
        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[AnimationGroup(*[Uncreate(x) for x in y]) for y in perm_group],
                lag_ratio = 0.1),
                sequence_length.animate.move_to(LEFT * 2.5),
            lag_ratio = 0.5),
            AnimationGroup(
                AnimationGroup(Create(brace_2), Write(total_2)),
                AnimationGroup(Create(brace_1), Write(total_1)),
                AnimationGroup(Create(brace_0), Write(total_0)),
            lag_ratio=0.2)
        )

        # show totals
        # self.play(
        #    sequence_length.animate.move_to(LEFT * 2.5),
        #    AnimationGroup(
        #        Create(total_2),
        #        Create(total_1),
        #        Create(total_0),
        #    lag_ratio=0.2)
        #)

        self.play(
            Circumscribe(Group(total_1, brace_1, *count_group[1:5]))
        )
            

        color_map = {
            "=": WHITE,
            "3": YELLOW,
            "2": PURPLE,
            "1": PURPLE,
            "0": PURPLE,
            "4": BLUE,
            "1 ": BLUE,
        }

        eulerian_number_2 = MathTex(r"A(", "3", ",", "2", ")", "=", "1 ", color=TEAL)
        eulerian_number_1 = MathTex(r"A(", "3", ",", "1", ")", "=", "4" , color=TEAL)
        eulerian_number_0 = MathTex(r"A(", "3", ",", "0", ")", "=", "1 ", color=TEAL)

        eulerian_number_2.set_color_by_tex_to_color_map(color_map)
        eulerian_number_1.set_color_by_tex_to_color_map(color_map)
        eulerian_number_0.set_color_by_tex_to_color_map(color_map)

        brace_2.put_at_tip(eulerian_number_2)
        brace_1.put_at_tip(eulerian_number_1)
        brace_0.put_at_tip(eulerian_number_0)

        # animate A(3, 1)
        self.play(
            AnimationGroup(
                *[AnimationGroup(
                    FadeOut(z[0]),
                    Write(VGroup(x[0], x[2], x[4], x[5])),
                    ReplacementTransform(sequence_length[2].copy(), x[1]),
                    AnimationGroup(*[ReplacementTransform(y_.copy(), x[3]) for y_ in y]),
                    ReplacementTransform(z[1], x[6]),
                    lag_ratio=0.2
                ) for x, y, z in zip(
                    [eulerian_number_1],
                    [[count_group[1:5]]],
                    [total_1]
                )], lag_ratio=0.2       
            )
        )

        # animated the other two
        self.play(
            AnimationGroup(
                *[AnimationGroup(
                    FadeOut(z[0]),
                    Write(VGroup(x[0], x[2], x[4], x[5])),
                    ReplacementTransform(sequence_length[2].copy(), x[1]),
                    AnimationGroup(*[ReplacementTransform(y_.copy(), x[3]) for y_ in y]),
                    ReplacementTransform(z[1], x[6]),
                    lag_ratio=0.2
                ) for x, y, z in zip(
                    [eulerian_number_2, eulerian_number_0],
                    [[count_group[0]], [count_group[5]]],
                    [total_2, total_0]
                )], lag_ratio=0.2       
            )
        )

        final_eulerian = VGroup(eulerian_number_0, eulerian_number_1, eulerian_number_2).copy().arrange(UP).move_to(ORIGIN)



        self.play(
            AnimationGroup(
            AnimationGroup(
            FadeOut(count_group),
            FadeOut(sequence_length),
            FadeOut(Group(brace_0, brace_1, brace_2)),
            FadeOut(ascent_title),
            FadeOut(ascent_line)),
            ReplacementTransform(VGroup(eulerian_number_0, eulerian_number_1, eulerian_number_2), final_eulerian),
            lag_ratio = 0.5)
        )

        self.play(Unwrite(final_eulerian))


        self.wait(2)


class Formulas(Scene):

    def construct(self):
        
        closed_form_title = Tex("Closed form formula")

        closed_form_math = MathTex(r"A(n, k) = \sum^k_{i = 0} {n + 1 \choose i} (k + 1 - i)^n")

        VGroup(closed_form_title, closed_form_math).arrange(DOWN).move_to(ORIGIN + UP * 1.5)

        recursive_title = Tex("Recursive formula")

        recursive_math = MathTex("A(n, k) = (k + 1) * T(n - 1, k) + (n - k) * T(n - 1, k - 1)")

        VGroup(recursive_title, recursive_math).arrange(DOWN).move_to(ORIGIN + DOWN * 1.5)

        self.play(
            Write(closed_form_title),
            Write(closed_form_math)
        )

        self.play(
            Write(recursive_title),
            Write(recursive_math)
        )

        self.wait(1)

        self.play(
            FadeOut(closed_form_title),
            FadeOut(closed_form_math)
        )

        # Create example sequence
        
        up_arrow = Arrow(start=ORIGIN, end=[.5, .8, 0], stroke_width=2, color=GREEN)
        down_arrow = Arrow(start=ORIGIN, end=[.5, -.8, 0], stroke_width=2, color=RED)

        sequence = VGroup(
            *[MathTex(x) for x in "2143"]
        )

        spacing = VGroup(
            *[MathTex(x) for x in "55555"]
        )

        sequence.arrange(RIGHT).move_to(ORIGIN + UP * 1.5)
        spacing.arrange(RIGHT).move_to(ORIGIN + UP * 1.5)

        up_spacing = spacing.copy().move_to(ORIGIN + UP * 2.25)

        self.play(
            Write(sequence)
        )

        new_number = MathTex("5")

        def space_sequence(spacing_list: List[int]):
            return [
                x.animate.move_to(spacing[y]) for x, y in zip(sequence, spacing_list)
            ]

        new_number.move_to(ORIGIN + UP * 2.25)

        self.play(
            Write(new_number)
        )

        self.play(
            new_number.animate.move_to(up_spacing[1]),
            *space_sequence([0, 2, 3, 4])
        )
 
        self.play(
            new_number.animate.move_to(up_spacing[4]),
            *space_sequence([0, 1, 2, 3])
        )

        self.play(
            new_number.animate.move_to(up_spacing[2]),
            *space_sequence([0, 1, 3, 4])
        )

        self.play(
            Unwrite(new_number),
            Unwrite(sequence),
            Unwrite(recursive_title),
            Unwrite(recursive_math)
        )

        self.wait(2)

class Triangle(Scene):

    def construct(self):
        
        def create_triangle(height=5, label=lambda x, y: ("A(", " " + str(x + 1), ",", str(y), ")"), color_map=lambda x, y: {str(y): PURPLE, " " + str(x + 1): YELLOW}, color=TEAL):

            group = []

            for i in range(height):
                n_group = []

                for j in range(i + 1):
                    a = MathTex(*label(i, j), color=color, tex_to_color_map=color_map(i, j))

                    n_group.append(a)

                group.append(VGroup(*n_group).arrange(RIGHT))

            group = VGroup(*group).arrange(DOWN)
            group.move_to(ORIGIN)

            return group

        def respace_triangle(triangle, space, height=1):
            for i in triangle:
                i.arrange_in_grid(col_widths=list(itertools.repeat(space, times=len(i))), col_alignment="c")
            triangle.arrange_in_grid(cols=1, row_widths = list(itertools.repeat(height, times=len(triangle))), row_alignment="c")


            return triangle
                

        def move_elements_triangle(triangle1, triangle2):
            for i, j in zip(flatten(triangle1), flatten(triangle2)):
                j.move_to(i)

            return triangle2

        def subtriangle(triangle):
            return VGroup(*[x[:-1] for x in triangle[1:]])

        def right_subtriangle(triangle):
            return VGroup(*[x[1:] for x in triangle[1:]])

        def flip_triangle(triangle):
            return VGroup(*[x[::-1] for x in triangle])

        triangle = create_triangle()
        
        triangle2 = create_triangle(label = lambda x, y: [eulerian(x+1, y)], color=BLUE, color_map=lambda x, y: None)
        triangle2 = move_elements_triangle(triangle, triangle2)

        original_triangle = triangle2.copy()

        #t2_copy = respace_triangle(triangle2.copy(), .5)

        triangle_plus_other = create_triangle(height=6, label = lambda x, y: [eulerian(x, y)], color=BLUE, color_map=lambda x, y: None)
        triangle_plus_other = respace_triangle(triangle_plus_other, .5)
        triangle_plus_other.move_to(ORIGIN + RIGHT * .25 + UP * .25)

        triangle_plus_other[0][0].set_color(WHITE)

        a00 = MathTex("A(", "0", ",", " 0", ")", color=TEAL, tex_to_color_map = {"0": YELLOW, " 0": PURPLE}).move_to(triangle_plus_other[0][0])
        qm = Tex("?", color=ORANGE).move_to(a00)

        nothing = MathTex("NOTH").move_to(ORIGIN + DOWN * 3)
        nothing_box = SurroundingRectangle(nothing)

        triangle_plus_other[0][0].set_color(ORANGE)
        for i in range(1, len(triangle_plus_other)):
            triangle_plus_other[i][i].set_color(RED)


        self.play(
            Write(triangle)
        )        

        self.play(
            ReplacementTransform(triangle, triangle2)
        )

        self.play(
            ReplacementTransform(triangle2, subtriangle(triangle_plus_other))
        )

        self.play(
            Write(a00)
        )

        self.play(
            ReplacementTransform(a00, qm)
        )

        self.play(
            Create(nothing_box)
        )

        self.play(
            Uncreate(nothing_box),
            ReplacementTransform(qm, triangle_plus_other[0][0])
        )

        self.play(
            AnimationGroup(*[
                Write(triangle_plus_other[x][x]) for x in range(1, len(triangle_plus_other))
            ], lag_ratio = 0.1)
        )

        #self.play(
        #    Write(SurroundingRectangle(VGroup(*[triangle_plus_other[x][x] for x in range(0, len(triangle_plus_other))])))
        #)


        center = triangle_plus_other[1][0].get_center()
        middle_line = Line(center + UP * 2, center + DOWN * 4, color=YELLOW)

        self.play(
            Create(middle_line)
        )

        self.play(
            Uncreate(middle_line)
        )

        flipped_triangle = flip_triangle(triangle_plus_other.copy()).move_to(LEFT * 4)
        flipped_triangle = respace_triangle(flipped_triangle, 0.5)
        flipped_triangle = flip_triangle(flipped_triangle) # to make the animations work


        self.play(
            triangle_plus_other.animate.move_to(RIGHT*4),
            ReplacementTransform(triangle_plus_other.copy(), flipped_triangle)
        )

        original_triangle = respace_triangle(original_triangle, 0.5)       
        original_triangle.move_to(UP * 2)

        self.play(
            Write(original_triangle)
        )

        original_oeis = Tex("A008292", color = YELLOW)
        original_oeis.next_to(original_triangle, direction=DOWN * 1.25)

        left_oeis = Tex("A123125", color = YELLOW)
        left_oeis.next_to(flipped_triangle, direction=DOWN * 1.25)

        right_oeis = Tex("A173018", color = YELLOW) 
        right_oeis.next_to(triangle_plus_other, direction=DOWN * 1.25)

        self.play(
            Write(original_oeis),
            Write(left_oeis),
            Write(right_oeis)
        )

        center_box = SurroundingRectangle(Group(original_triangle, original_oeis))

        self.play(
            Indicate(subtriangle(flipped_triangle)),
            Indicate(original_triangle),
            Indicate(subtriangle(triangle_plus_other))
        )

        self.play(
            Write(center_box),
        )

        self.play(
            Unwrite(center_box),
            Unwrite(flipped_triangle),
            Unwrite(triangle_plus_other),
            Unwrite(original_oeis),
            Unwrite(left_oeis),
            Unwrite(right_oeis),
            original_triangle.animate.move_to(ORIGIN)
        )
        
        self.wait(2)


class TriangleProperties(Scene):

    def construct(self):
        def create_triangle(height=5, label=lambda x, y: ("A(", " " + str(x + 1), ",", str(y), ")"), color_map=lambda x, y: {str(y): PURPLE, " " + str(x + 1): YELLOW}, color=TEAL):

            group = []

            for i in range(height):
                n_group = []

                for j in range(i + 1):
                    a = MathTex(*label(i, j), color=color, tex_to_color_map=color_map(i, j))

                    n_group.append(a)

                group.append(VGroup(*n_group).arrange(RIGHT))

            group = VGroup(*group).arrange(DOWN)
            group.move_to(ORIGIN)

            return group

        def respace_triangle(triangle, space, height=1):
            for i in triangle:
                i.arrange_in_grid(col_widths=list(itertools.repeat(space, times=len(i))), col_alignment="c")
            triangle.arrange_in_grid(cols=1, row_widths = list(itertools.repeat(height, times=len(triangle))), row_alignment="c")


            return triangle
                

        def move_elements_triangle(triangle1, triangle2):
            for i, j in zip(flatten(triangle1), flatten(triangle2)):
                j.move_to(i)

            return triangle2

        def subtriangle(triangle):
            return VGroup(*[x[:-1] for x in triangle[1:]])

        def right_subtriangle(triangle):
            return VGroup(*[x[1:] for x in triangle[1:]])

        def flip_triangle(triangle):
            return VGroup(*[x[::-1] for x in triangle])

        up_arrow = Arrow(start=ORIGIN, end=[.5, .8, 0], stroke_width=2, color=GREEN)
        down_arrow = Arrow(start=ORIGIN, end=[.5, -.8, 0], stroke_width=2, color=RED)
        def create_sequence(sequence):
           
            group = []
            last = None
            for i in sequence:
                if last:
                    group.append(up_arrow.copy() if i > last else down_arrow.copy())

                group.append(MathTex(str(i)))

                last = i

            group = VGroup(*group).arrange(RIGHT * 0.8)

            return VGroup(*group)

        
        triangle = create_triangle(height=5, label = lambda x, y: [eulerian(x + 1, y)], color=BLUE, color_map=lambda x, y: None)
        triangle = respace_triangle(triangle, 0.5)
        triangle.move_to(ORIGIN)

        self.add(triangle)

        symmetrical_line = Line(UP * 2, DOWN * 2, color = YELLOW)

        self.play(
            Create(symmetrical_line)
        )

        self.play(
            Uncreate(symmetrical_line)
        )

        sequence = create_sequence([3, 1, 5, 4, 2, 6]).move_to(UP)

        self.play(
            FadeOut(triangle),
            Write(sequence)
        )

        reversed_sequence = create_sequence([6, 2, 4, 5, 1, 3]).move_to(DOWN)

        self.play(
            ReplacementTransform(sequence[::1].copy(), reversed_sequence[::-1]),
            #Write(reversed_sequence[1::2]) 
        )

        linking_arrows = []
        for i in range(5):
            linking_arrows.append(Arrow(start=sequence[1 + 2 * i].get_center() + DOWN * .25, end=reversed_sequence[-2 - 2 * i].get_center() + UP * .25, stroke_width=5, color=YELLOW))
        linking_arrows = VGroup(*linking_arrows)

        self.play(
            Write(linking_arrows[0]),
            Write(linking_arrows[2]),
            Write(linking_arrows[3])
        )

        self.play(
            Unwrite(linking_arrows[0]),
            Unwrite(linking_arrows[2]),
            Unwrite(linking_arrows[3])
        )

        self.play(
            Write(linking_arrows[1]),
            Write(linking_arrows[4]),
            #Write(linking_arrows[5])
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Unwrite(linking_arrows[1]),
                    Unwrite(linking_arrows[4]),
                ),
                AnimationGroup(
                    Unwrite(sequence),
                    Unwrite(reversed_sequence)
                ),
            lag_ratio = 0.3)
        )

        self.play(
            FadeIn(triangle)
        )

        row_boxes = Group(*[
            SurroundingRectangle(x) for x in triangle
        ])

        self.play(
            AnimationGroup(
                *[Circumscribe(x) for x in triangle],
            lag_ratio = 0.1)
        )

        sums = VGroup(*[MathTex(f"{factorial(x + 1)} = {x + 1}", "!", tex_to_color_map = {"!": TEAL}) for x in range(5)])
        for x, y in zip(triangle, sums):
            y.next_to(x, direction=RIGHT)
            y.set_x(2)

        self.play(
            triangle.animate.move_to(ORIGIN + LEFT * 1),
            AnimationGroup(
                *[ReplacementTransform(x.copy(), y) for x, y in zip(triangle, sums)]
            , lag_ratio = 0.2)
        )

        vertical_row = triangle[3].copy().arrange(DOWN * 1.5).move_to(3 * LEFT + ORIGIN)

        self.play(
            FadeOut(triangle[0]),
            FadeOut(triangle[1]),
            FadeOut(triangle[2]),
            FadeOut(triangle[4]),
            ReplacementTransform(triangle[3], vertical_row),
            FadeOut(sums)
        )

        braces = VGroup(*[Brace(x, direction=RIGHT) for x in vertical_row])
        labels = VGroup(*[Tex(eulerian(4, x), " permutations for ", " " + str(x), " ascents", tex_to_color_map = {str(eulerian(4, x)): BLUE, " " + str(x): PURPLE}) for x in range(4)])

        primary_label = Tex("24", " permutations for ", "all", " ascents",
                            tex_to_color_map = {"24": BLUE, "all": PURPLE})

        fourfact = MathTex("4!", color=BLUE).move_to(primary_label[0])

        for b, l in zip(braces, labels):
            l.next_to(b, direction=RIGHT)

        self.play(
            Create(braces),
            Write(labels)
        )

        self.play(
            FadeOut(vertical_row),
            FadeOut(braces),
            ReplacementTransform(labels, primary_label)
        )

        self.play(
            Transform(primary_label[0], fourfact)
        )

        self.play(
            Unwrite(primary_label)
        )
            

        # sum of rows

        self.wait(2)

class Ending(Scene):
    def construct(self):

        title = Tex("Questions?", font_size=96)

        line = Line(start=ORIGIN, end=[10, 0, 0])

        author = VGroup(Tex(r"Animated using manimce").scale(0.75), Tex("Put together using Shotcut").scale(0.75), Tex("Code for the animation is available on my github:").scale(0.75), Tex("github.com/plasmaofthedawn/euleriananimation").scale(0.75)).arrange(DOWN)

        Group(title, line, author).arrange(DOWN * 2)
        
        self.play(
            AnimationGroup(Write(title), Create(line), Write(author), lag_ratio=0.1)
        )

        self.wait(1)

        self.play(
            Unwrite(title, reverse=False), Uncreate(line), Unwrite(author, reverse=False)
        )


class Ank(Scene):
    def construct(self):

        color_map = {
            "=": WHITE,
            "n": YELLOW,
            "k": PURPLE,
            "n-k": PURPLE,
        }

        eulerian_number_2 = MathTex(r"A(", "n", ",", "k", ")", "=", "A(", "n", ",", "n - k - 1", ")", color=TEAL)

        eulerian_number_2.set_color_by_tex_to_color_map(color_map)

        self.play(Write(eulerian_number_2))
        self.play(Unwrite(eulerian_number_2))

        
class OutsideOnes(Scene):
    def construct(self):
        
        def create_triangle(height=5, label=lambda x, y: ("A(", " " + str(x + 1), ",", str(y), ")"), color_map=lambda x, y: {str(y): PURPLE, " " + str(x + 1): YELLOW}, color=TEAL):

            group = []

            for i in range(height):
                n_group = []

                for j in range(i + 1):
                    a = MathTex(*label(i, j), color=color, tex_to_color_map=color_map(i, j))

                    n_group.append(a)

                group.append(VGroup(*n_group).arrange(RIGHT))

            group = VGroup(*group).arrange(DOWN)
            group.move_to(ORIGIN)

            return group

        def respace_triangle(triangle, space, height=1):
            for i in triangle:
                i.arrange_in_grid(col_widths=list(itertools.repeat(space, times=len(i))), col_alignment="c")
            triangle.arrange_in_grid(cols=1, row_widths = list(itertools.repeat(height, times=len(triangle))), row_alignment="c")


            return triangle
                

        def move_elements_triangle(triangle1, triangle2):
            for i, j in zip(flatten(triangle1), flatten(triangle2)):
                j.move_to(i)

            return triangle2

        def subtriangle(triangle):
            return VGroup(*[x[:-1] for x in triangle[1:]])

        def right_subtriangle(triangle):
            return VGroup(*[x[1:] for x in triangle[1:]])

        def flip_triangle(triangle):
            return VGroup(*[x[::-1] for x in triangle])

        up_arrow = Arrow(start=ORIGIN, end=[.5, .8, 0], stroke_width=2, color=GREEN)
        down_arrow = Arrow(start=ORIGIN, end=[.5, -.8, 0], stroke_width=2, color=RED)
        def create_sequence(sequence):
           
            group = []
            last = None
            for i in sequence:
                if last:
                    group.append(up_arrow.copy() if i > last else down_arrow.copy())

                group.append(MathTex(str(i)))

                last = i

            group = VGroup(*group).arrange(RIGHT * 0.8)

            return VGroup(*group)

        
        triangle = create_triangle(height=5, label = lambda x, y: [eulerian(x + 1, y)], color=BLUE, color_map=lambda x, y: None)
        triangle = respace_triangle(triangle, 0.5)
        triangle.move_to(ORIGIN)

        self.play(
            FadeIn(triangle)
        )

        self.play(
            Indicate(VGroup(*[triangle[x][x] for x in range(5)], *[triangle[x][0] for x in range(5)]))
        )

        dec_seq = create_sequence([6, 5, 4, 3, 2, 1]).move_to(UP)
        inc_seq = create_sequence([1, 2, 3, 4, 5, 6]).move_to(DOWN)

        self.play(
            FadeOut(triangle),
            Write(dec_seq)
        )

        self.play(
            Write(inc_seq)
        )

        self.play(
            Unwrite(dec_seq),
            Unwrite(inc_seq),
        )

