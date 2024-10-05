from loguru import logger
from shiny import module, reactive, render, ui

from core.converters import Converters
from core.di_container import DiContainer
from models.my_model import MyModel


@module.ui
def my_module_ui():
    return ui.div(
        ui.input_slider("sld_input", "Slider value", min=1, max=10, value=2),
        ui.output_text_verbatim("txt_output"),
        ui.output_data_frame("tbl_output"),
    )


@module.server
def my_module_server(input, output, session, di_container: DiContainer):
    fib_entity = reactive.value(MyModel())
    fib_history = []

    @reactive.calc
    def get_fib():
        x = input.sld_input()

        logger.info(f"Calculating fibonacci for {x}")

        fib = di_container.my_service.get_fibonacci(x)
        logger.info(f"Fibonacci for {x} is {fib}")

        mymodel = MyModel()
        mymodel.set_fib(x, fib)
        fib_entity.set(mymodel)
        return fib

    @render.text
    def txt_output():
        return f"Fibonacci: {get_fib()}"

    @render.data_frame
    def tbl_output():
        data = fib_entity.get()
        fib_history.append(data)
        if data is not None:
            return render.DataGrid(
                Converters.convert_objectlist_to_dataframe(fib_history), width="100%"
            )
        return None
