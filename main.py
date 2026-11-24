import matplotlib.pyplot as plt
from dataclasses import dataclass
from bakery import assert_equal
from drafter import *

set_website_title("Economics Graph Maker")
set_site_information(
    author="William Ciecko",
    description="Makes custom and accurate economics graphs based on the introduction to microeconomics curriculum",
    sources="Thanks to the Drafter docs, my teacher, previous code, BlockPy, and matplotlib docs",
    planning=["plan.pdf", "design.pdf", "feedback.pdf"],
    links=["https://github.com/cieckowilliam/economics-graph-maker"])
hide_debug_information()
set_website_framed(False)

@dataclass
class Graph:
    title: str
    graph_type: str
    supply_slope: float
    demand_slope: float
    initial_supply: float
    initial_demand: float
    first_extra: float
    second_extra: float
    market: str
    price: str
    quantity: str

@dataclass
class State:
    title: str
    graph_type: str
    supply_slope: float
    demand_slope: float
    initial_supply: float
    initial_demand: float
    first_extra: float
    second_extra: float
    market: str
    price: str
    quantity: str
    saved_graphs: list[Graph]
    
GRAPH_TYPES = ["Supply and Demand", "Tariff", "Negative Externality"]

def draw_graph(state: State) -> None:
    """
    Description: Draws the graph of the current state onto matplotlib
    by clearing the figure, then plotting line points and shaded areas based on the current state
    Arguments: state(State): The current state which holds the graph type and values
    Returns: None: draws onto matplotlib figure but does not return it
    """
    
    plt.clf()
    demand_slope = state.demand_slope
    supply_slope = state.supply_slope

    initial_demand = state.initial_demand
    initial_supply = state.initial_supply
    
    market = state.market
    price = state.price
    quantity = state.quantity
    
    if state.graph_type == "Supply and Demand":
        equilibrium_quantity = (initial_supply - initial_demand) / (demand_slope - supply_slope)
        equilibrium_price = supply_slope * equilibrium_quantity + initial_supply

        xs = [0, 2 * equilibrium_quantity]

        dy = [demand_slope * x + initial_demand for x in xs]
        sy = [supply_slope * x + initial_supply for x in xs]

        plt.plot(xs, dy, label = "Demand = MB", color = "red")
        plt.plot(xs, sy,label = "Supply = MC", color = "blue" )
        
        plt.hlines(equilibrium_price, 0, equilibrium_quantity, linestyles = "dashed", color = "black")
        plt.vlines(equilibrium_quantity, 0, equilibrium_price, linestyles = "dashed", color = "black")
        plt.scatter(equilibrium_quantity, equilibrium_price, zorder = 10, color = "black", label = "Equilibrium")
        
        plt.fill([0, equilibrium_quantity, 0],
                 [initial_demand, equilibrium_price, equilibrium_price],
                 color = "lightcoral",
                 label = "Consumer Surplus")
        plt.fill([0, equilibrium_quantity, 0],
                 [initial_supply, equilibrium_price, equilibrium_price],
                 color = "skyblue",
                 label = "Producer Surplus")
        
        plt.legend(loc = "upper center")
        plt.title(market + " Market")
        plt.xlabel("Quantity(" + quantity + ")")
        plt.ylabel("Price(" + price + ")")
        plt.ylim(bottom = 0)
        plt.margins(0.025)
        
    elif state.graph_type == "Tariff":
        equilibrium_quantity = (initial_supply - initial_demand) / (demand_slope - supply_slope)
        equilibrium_price = supply_slope * equilibrium_quantity + initial_supply

        world_price = state.first_extra
        tariff_price = state.second_extra
        
        seller_trade_quantity = (world_price - initial_supply) / supply_slope
        seller_tariff_quantity = (tariff_price - initial_supply) / supply_slope
        buyer_tariff_quantity = (tariff_price - initial_demand) / demand_slope
        buyer_trade_quantity = (world_price - initial_demand) / demand_slope
        
        xs = [0, buyer_trade_quantity]

        dy = [demand_slope * x + initial_demand for x in xs]
        sy = [supply_slope * x + initial_supply for x in xs]

        plt.plot(xs, dy, label = "Demand = MB", color = "red")
        plt.plot(xs, sy,label = "Supply = MC", color = "blue" )
        plt.scatter(equilibrium_quantity, equilibrium_price, zorder = 10, color = "black", label = "Equilibrium")
        
        plt.hlines(equilibrium_price, 0, equilibrium_quantity, linestyles = "dashed", color = "black")
        plt.vlines(equilibrium_quantity, 0, equilibrium_price, linestyles = "dashed", color = "black")
        
        plt.hlines(tariff_price, 0, buyer_trade_quantity, linestyles = "dashed", color = "black")
        plt.hlines(world_price, 0, buyer_trade_quantity, linestyles = "dashed", color = "black")
        
        plt.vlines(seller_trade_quantity, 0, world_price, linestyles = "dashed", color = "black")
        plt.vlines(seller_tariff_quantity, 0, tariff_price, linestyles = "dashed", color = "black")
        plt.vlines(buyer_tariff_quantity, 0, tariff_price, linestyles = "dashed", color = "black")
        plt.vlines(buyer_trade_quantity, 0, world_price, linestyles = "dashed", color = "black")
        
        plt.fill([0, buyer_tariff_quantity, 0],
                 [initial_demand, tariff_price, tariff_price],
                 color = "lightcoral",
                 label = "Consumer Surplus")
        plt.fill([0, seller_tariff_quantity, 0],
                 [initial_supply, tariff_price, tariff_price],
                 color = "skyblue",
                 label = "Producer Surplus")
        plt.fill([seller_tariff_quantity, buyer_tariff_quantity, buyer_tariff_quantity, seller_tariff_quantity],
                 [world_price, world_price, tariff_price, tariff_price],
                 color = "lightgreen",
                 label = "Government Revenue")
        plt.fill([buyer_trade_quantity, buyer_tariff_quantity, buyer_tariff_quantity],
                 [world_price, world_price, tariff_price],
                 color = "khaki")
        plt.fill([seller_trade_quantity, seller_tariff_quantity, seller_tariff_quantity],
                 [world_price, world_price, tariff_price],
                 color = "khaki",
                 label = "Dead Weight Loss")
        
        plt.legend(loc = "upper right")
        plt.title(market + " Market")
        plt.xlabel("Quantity(" + quantity + ")")
        plt.ylabel("Price(" + price + ")")
        plt.ylim(bottom = 0)
        plt.ylim(top = initial_demand)

    elif state.graph_type == "Negative Externality":
        externality_slope = state.first_extra
        initial_externality = state.second_extra

        equilibrium_quantity = (initial_supply - initial_demand) / (demand_slope - supply_slope)
        equilibrium_price = supply_slope * equilibrium_quantity + initial_supply
        
        socially_optimal_quantity = (initial_externality - initial_demand) / (demand_slope - externality_slope)
        socially_optimal_price = externality_slope * socially_optimal_quantity + initial_externality
        peak_social_cost = externality_slope * equilibrium_quantity + initial_externality

        xs = [0, 2 * equilibrium_quantity]

        dy = [demand_slope * x + initial_demand for x in xs]
        sy = [supply_slope * x + initial_supply for x in xs]
        ey = [externality_slope * x + initial_externality for x in xs]

        plt.plot(xs, dy, label = "Demand = MB", color = "red")
        plt.plot(xs, sy,label = "Supply = MPC", color = "blue" )
        plt.plot(xs, ey,label = "MSC", color = "black" )
        
        plt.hlines(equilibrium_price, 0, equilibrium_quantity, linestyles = "dashed", color = "black")
        plt.vlines(equilibrium_quantity, 0, peak_social_cost, linestyles = "dashed", color = "black")
        plt.scatter(equilibrium_quantity, equilibrium_price, zorder = 10, color = "black")
        
        plt.hlines(socially_optimal_price, 0, socially_optimal_quantity, linestyles = "dashed", color = "black")
        plt.vlines(socially_optimal_quantity, 0, socially_optimal_price, linestyles = "dashed", color = "black")
        plt.scatter(socially_optimal_quantity, socially_optimal_price, zorder = 10, color = "black")

        plt.fill([0, 0, equilibrium_quantity],
                 [initial_demand, equilibrium_price, equilibrium_price],
                 color = "lightcoral",
                 label = "Consumer Surplus")
        plt.fill([0, 0, equilibrium_quantity],
                 [initial_supply, equilibrium_price, equilibrium_price],
                 color = "skyblue",
                 label = "Producer Surplus")
        plt.fill([socially_optimal_quantity, equilibrium_quantity, equilibrium_quantity],
                 [socially_optimal_price, equilibrium_price, peak_social_cost],
                 color = "khaki",
                 label = "Dead Weight Loss")
            
        plt.legend(loc = "upper center")
        plt.title(market + " Market")
        plt.xlabel("Quantity(" + quantity + ")")
        plt.ylabel("Price(" + price + ")")
        plt.ylim(bottom = 0)
        
def is_number(number: str) -> bool:
    """
    Description: Determines whether a string input is a number
    Arguments: str: A user input of string type that should be a number
    Returns: bool: whether or not the string is a number
    """
    if not number:
        return False
    if number == ".":
        return False
    if number == "-":
        return False
    
    value = ""
    if number[0] == "-":
        value = number[1:]
    else:
        value = number
        
    parts = value.split(".")
    
    if len(parts) > 2:
        return False
    else:
        for part in parts:
            numbers_only = True
            for character in part:
                if character in "0123456789":
                    numbers_only = numbers_only and True
                else:
                    numbers_only = numbers_only and False
        if numbers_only == False:
            return False
        else:
            return True

@route
def index(state: State) -> Page:
    """
    Description: Creates a home page with the title and start button 
    Arguments: state(State): The current state 
    Returns: Page: A page with a header button that leads to select_graph
    """
    return Page(state, [
        Header("Economics Graph Maker", 1),
        Button("Start", select_graph),
        Button("Saved Graphs", view_saved_graphs)])

@route
def select_graph(state: State) -> Page:
    """
    Description: Creates a page for the user to pick a type of graph
    Arguments: state(State): The current state used for the SelectBox
    Returns: Page: A page with a SelectBox of GRAPH_TYPES and a home and next button
    """
    return Page(state, [
        Header("Select Graph Type", 2),
        "Graph Type:",
        SelectBox("graph_type", GRAPH_TYPES, state.graph_type),
        Button("Next", save_type),
        Button("Home", index)])

@route
def save_type(state: State, graph_type: str) -> Page:
    """
    Description: Saves the selected graph type to the state, then shows the input page 
    Arguments: state(State): The current state that is being modified
        graph_type: str: The graph type the user selected
    Returns: Page: The page that is produced by enter_inputs
    """
    state.graph_type = graph_type
    return(enter_inputs(state))

@route
def enter_inputs(state: State) -> Page:
    """
    Description: Creates a page with text boxes to enter inputs for the graphs
    Gives every graph inputs for supply and demand slope and initial values
    Conditionally assigns secondary value inputs for more complex graphs
    Arguments: state(State): The current state used for default text box values
    Returns: Page: A page with a make graph button that conditionally goes to
    save_inputs or save_extra_inputs based on the graph type
    """
    input_fields = [
        Header("Input Graph Information", 2),
        "Title:", TextBox("title", state.title), LineBreak(),
        "Supply Slope:", TextBox("supply_slope", state.supply_slope), LineBreak(),
        "Demand Slope:", TextBox("demand_slope", state.demand_slope), LineBreak(),
        "Initial Supply:", TextBox("initial_supply", state.initial_supply), LineBreak(),
        "Initial Demand:", TextBox("initial_demand", state.initial_demand), LineBreak(),
        "Market:", TextBox("market", state.market), LineBreak(),
        "Unit Price:", TextBox("price", state.price), LineBreak(),
        "Unit Quantity:", TextBox("quantity", state.quantity), LineBreak()]
    
    if state.graph_type == "Tariff":
        input_fields += ["World Price", TextBox("first_extra", state.first_extra), LineBreak(),
                         "Tariff Price", TextBox("second_extra", state.second_extra), LineBreak()]
        return Page(state, input_fields + [Button("Make Graph", save_extra_inputs), Button("Home", index)])
    
    if state.graph_type == "Negative Externality":
        input_fields += ["MSC Slope", TextBox("first_extra", state.first_extra,), LineBreak(),
                         "MSC Intercept", TextBox("second_extra", state.second_extra), LineBreak()]
        return Page(state, input_fields + [Button("Make Graph", save_extra_inputs), Button("Home", index)])
    return Page(state, input_fields + [Button("Make Graph", save_inputs), Button("Home", index)])
    
@route
def save_inputs(state: State, title: str,
                supply_slope: str, demand_slope: str, initial_supply: str, initial_demand: str,
                market: str, price: str, quantity: str) -> Page:
    """
    Description: Saves basic graph inputs to the state and shows the graph
    Arguments: state(State): The current state which is being modified
        title: str: graph title
        supply_slope: str: supply curve slope
        demand_slope: str: demand curve slope
        initial_supply: str: initial point for supply curve
        initial_demand: str: initial point for demand curve
        market: str: the product market for which the graph represents
        price: str: the measure of price (ex., $)
        quantity: str: the measure of quantity  (ex., 1000 barrels of oil)
    Returns: Page: A page produced by show_graph
    """
    if len(title) > 50:
        return Page(state, ["Input Length Error: title length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif len(market) > 25:
        return Page(state, ["Input Length Error: market length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif len(price) > 25:
        return Page(state, ["Input Length Error: price length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif len(quantity) > 25:
        return Page(state, ["Input Length Error: quantity length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(supply_slope):
        return Page(state, ["Input Type Error: supply slope must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(demand_slope):
        return Page(state, ["Input Type Error: demand slope must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(initial_supply):
        return Page(state, ["Input Type Error: initial supply must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(initial_demand):
        return Page(state, ["Input Type Error: initial demand must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif float(supply_slope) <= 0:
        return Page(state, ["Slope Error: supply slope must be positive", LineBreak(),
                            Button("Back", enter_inputs)])
    elif float(demand_slope) >= 0:
        return Page(state, ["Slope Error: demand slope must be negative", LineBreak(),
                            Button("Back", enter_inputs)])
    else:
        state.title = title
        state.supply_slope = float(supply_slope)
        state.demand_slope = float(demand_slope)
        state.initial_supply = float(initial_supply)
        state.initial_demand = float(initial_demand)
        state.market = market
        state.price = price
        state.quantity = quantity
        return show_graph(state)
    
@route
def save_extra_inputs(state: State, title: str,
                      supply_slope: str, demand_slope: str, initial_supply: str, initial_demand: str,
                      first_extra: str, second_extra: str,
                      market: str, price: str, quantity: str) -> Page:
    """
    Description: Saves more complex graph inputs to the state and shows the graph
    Arguments: state(State): The current state which is being modified
        title: str: graph title
        supply_slope: str: supply curve slope
        demand_slope: str: demand curve slope
        initial_supply: str: initial point for supply curve
        initial_demand: str: initial point for demand curve
        first_extra: str: world price or slope of MSC curve
        second_extra: str: tariff price or initial point of MSC curve
        market: str: the product market for which the graph represents
        price: str: the measure of price (ex., $)
        quantity: str: the measure of quantity  (ex., 1000 barrels of oil)
    Returns: Page: A page produced by show_graph
    """
    if len(title) > 50:
        return Page(state, ["Input Length Error: title length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif len(market) > 25:
        return Page(state, ["Input Length Error: market length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif len(price) > 25:
        return Page(state, ["Input Length Error: price length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif len(quantity) > 25:
        return Page(state, ["Input Length Error: quantity length too long", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(supply_slope):
        return Page(state, ["Input Type Error: supply slope must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(demand_slope):
        return Page(state, ["Input Type Error: demand slope must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(initial_supply):
        return Page(state, ["Input Type Error: initial supply must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(initial_demand):
        return Page(state, ["Input Type Error: initial demand must be a number", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(first_extra):
        return Page(state, ["Input Type Error", LineBreak(),
                            Button("Back", enter_inputs)])
    elif not is_number(second_extra):
        return Page(state, ["Input Type Error", LineBreak(),
                            Button("Back", enter_inputs)])
    elif float(supply_slope) <= 0:
        return Page(state, ["Slope Error: supply slope must be positive", LineBreak(),
                            Button("Back", enter_inputs)])
    elif float(demand_slope) >= 0:
        return Page(state, ["Slope Error: demand slope must be negative", LineBreak(),
                            Button("Back", enter_inputs)])
    else:
        state.title = title
        state.supply_slope = float(supply_slope)
        state.demand_slope = float(demand_slope)
        state.initial_supply = float(initial_supply)
        state.initial_demand = float(initial_demand)
        state.first_extra = float(first_extra)
        state.second_extra = float(second_extra)
        state.market = market
        state.price = price
        state.quantity = quantity
        return show_graph(state)

    
@route
def show_graph(state: State) -> Page:
    """
    Description: Draws and displays the current graph
    Arguments: state(State): The current state of the graph
    Returns: Page: A page with the plotted graph and
    buttons to save graphs, view saved graphs, and go home
    """
    draw_graph(state)
    return Page(state, [
        Header(state.title, 2),
        MatPlotLibPlot(), LineBreak(),
        Button("Save Graph", save_graph),
        Button("Saved Graphs", view_saved_graphs),
        Button("Home", index)])

@route
def save_graph(state: State) -> Page:
    """
    Description: Adds current graph to list of saved graphs
    Arguments: state(State): The current state of the graph
    Returns: Page: A page produced by view_saved_graphs
    """
    new_graph = Graph(state.title, state.graph_type,
                      state.supply_slope, state.demand_slope, state.initial_supply, state.initial_demand,
                      state.first_extra, state.second_extra,
                      state.market, state.price, state.quantity)
    state.saved_graphs.append(new_graph)
    return view_saved_graphs(state)

@route
def view_saved_graphs(state: State) -> Page:
    """
    Description: Creates a page listing titles of saved graphs 
    Arguments: state(State): The current state 
    Returns: Page: A page with a home button, SelectBox, and open button featuring all the saved graphs
    Displays "No Saved Graphs" if there are none in the list
    """
    if len(state.saved_graphs) == 0:
        return Page(state, [
            Header("Saved Graphs", 2),
            "No Saved Graphs",
            Button("Home", index)])
    
    titles = []
    for graph in state.saved_graphs:
        titles.append(graph.title)
        
    return Page(state, [
        Header("Saved Graphs", 2),
        SelectBox("choice", titles, titles[0]),
        Button("Open", open_saved_graphs),
        Button("Home", index)])
    
@route
def open_saved_graphs(state: State, choice: str) -> Page:
    """
    Description: Loads selected graphs with title into state and shows it 
    Arguments: state(State): The current state which is being modified
        choice: str: the title of the saved graph
    Returns: Page: A page produced by show_graph of the graph with the title
    """
    for graph in state.saved_graphs:
        if graph.title == choice:
            state.title = graph.title
            state.graph_type = graph.graph_type
            state.supply_slope = graph.supply_slope
            state.demand_slope = graph.demand_slope
            state.initial_supply = graph.initial_supply
            state.initial_demand = graph.initial_demand
            state.first_extra = graph.first_extra
            state.second_extra = graph.second_extra
            state.market = graph.market
            state.price = graph.price
            state.quantity = graph.quantity
    return show_graph(state)

assert_equal(draw_graph(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", [])), None)

assert_equal(is_number("1.0"), True)
assert_equal(is_number("1"), True)
assert_equal(is_number("2.a"), False)
assert_equal(is_number("-1"), True)
assert_equal(is_number("-1.3"), True)
assert_equal(is_number("-a"), False)
assert_equal(is_number("z.z"), False)
assert_equal(is_number(""), False)
assert_equal(is_number("."), False)
assert_equal(is_number("-"), False)

assert_equal(index(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", [])),
             Page(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", []), [
                 Header("Economics Graph Maker", 1),
                 Button("Start", select_graph),
                 Button("Saved Graphs", view_saved_graphs)]))

assert_equal(select_graph(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", [])),
             Page(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", []), [
                 Header("Select Graph Type", 2),
                 "Graph Type:",
                 SelectBox("graph_type", GRAPH_TYPES, "Supply and Demand"),
                 Button("Next", save_type),
                 Button("Home", index)]))

assert_equal(save_type(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons", []), "Tariff"),
             Page(State("My Graph", "Tariff", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons", []), [
                 Header("Input Graph Information", 2),
                 "Title:", TextBox("title", "My Graph"), LineBreak(),
                 "Supply Slope:", TextBox("supply_slope", 1.0), LineBreak(),
                 "Demand Slope:", TextBox("demand_slope", -1.0), LineBreak(),
                 "Initial Supply:", TextBox("initial_supply", 2.0), LineBreak(),
                 "Initial Demand:", TextBox("initial_demand", 20.0), LineBreak(),
                 "Market:", TextBox("market", "Gas"), LineBreak(),
                 "Unit Price:", TextBox("price", "$"), LineBreak(), 
                 "Unit Quantity:", TextBox("quantity", "gallons"), LineBreak(),
                 "World Price", TextBox("first_extra", 5.0), LineBreak(),
                 "Tariff Price", TextBox("second_extra", 8.0), LineBreak(),
                 Button("Make Graph", save_extra_inputs),
                 Button("Home", index)]))

assert_equal(enter_inputs(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons", [])),
             Page(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons", []), [
                 Header("Input Graph Information", 2),
                 "Title:", TextBox("title", "My Graph"), LineBreak(),
                 "Supply Slope:", TextBox("supply_slope", 1.0), LineBreak(),
                 "Demand Slope:", TextBox("demand_slope", -1.0), LineBreak(),
                 "Initial Supply:", TextBox("initial_supply", 2.0), LineBreak(),
                 "Initial Demand:", TextBox("initial_demand", 20.0), LineBreak(),
                 "Market:", TextBox("market", "Gas"), LineBreak(), 
                 "Unit Price:", TextBox("price", "$"), LineBreak(),
                 "Unit Quantity:", TextBox("quantity", "gallons"), LineBreak(),
                 Button("Make Graph", save_inputs),
                 Button("Home", index)]))

assert_equal(save_inputs(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", []),
                         "New Graph", "2.0", "-3.0", "1.0", "30.0", "Gas", "$", "gallons"),
             Page(State("New Graph", "Supply and Demand", 2.0, -3.0, 1.0, 30.0, 0.0, 0.0, "Gas", "$", "gallons", []), [
                 Header("New Graph", 2),
                 MatPlotLibPlot(), LineBreak(),
                 Button("Save Graph", save_graph),
                 Button("Saved Graphs", view_saved_graphs),
                 Button("Home", index)]))

assert_equal(save_extra_inputs(State("My Graph", "Tariff", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", []),
                         "New Graph", "1.0", "-1.0", "2.0", "20.0", "5.0", "8.0", "Gas", "$", "gallons"),
             Page(State("New Graph", "Tariff", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons", []), [
                 Header("New Graph", 2),
                 MatPlotLibPlot(), LineBreak(),
                 Button("Save Graph", save_graph),
                 Button("Saved Graphs", view_saved_graphs),
                 Button("Home", index)]))

assert_equal(show_graph(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", [])),
             Page(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", []), [
                 Header("My Graph", 2),
                 MatPlotLibPlot(), LineBreak(),
                 Button("Save Graph", save_graph),
                 Button("Saved Graphs", view_saved_graphs),
                 Button("Home", index)]))

assert_equal(save_graph(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", [])),
             Page(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons",
                        [Graph("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons")]), [
                 Header("Saved Graphs", 2),
                 SelectBox("choice", ["My Graph"], "My Graph"),
                 Button("Open", open_saved_graphs),
                 Button("Home", index)]))

assert_equal(view_saved_graphs(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons",
                              [Graph("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons")])),
             Page(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons",
                        [Graph("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons")]), [
                 Header("Saved Graphs", 2),
                 SelectBox("choice", ["My Graph"], "My Graph"),
                 Button("Open", open_saved_graphs),
                 Button("Home", index)]))

assert_equal(open_saved_graphs(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons",
                              [Graph("New Graph", "Tariff", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons")]),
                               "New Graph"),
             Page(State("New Graph", "Tariff", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons",
                        [Graph("New Graph", "Tariff", 1.0, -1.0, 2.0, 20.0, 5.0, 8.0, "Gas", "$", "gallons")]), [
                 Header("New Graph", 2),
                 MatPlotLibPlot(), LineBreak(),
                 Button("Save Graph", save_graph),
                 Button("Saved Graphs", view_saved_graphs),
                 Button("Home", index)]))

start_server(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, "Gas", "$", "gallons", []))
