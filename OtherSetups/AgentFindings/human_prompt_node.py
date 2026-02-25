"""
Custom ComfyUI node for generating human‑figure prompts
------------------------------------------------------

This node is designed to simplify the creation of prompts for full‑body
generation of human subjects with realistic anatomy and skin details.
It exposes a series of dropdown menus and text boxes that allow the
user to specify common demographic and physical characteristics such as
gender, ethnicity, age range, height and body type.  Additional options
control the level of muscularity, whether the subject is nude or
clothed, a custom clothing description, and whether studio lighting
should be used.  From these inputs the node synthesizes a positive
prompt describing the subject in natural language as well as a
complementary negative prompt to avoid undesirable artefacts.

The node returns two strings: a positive prompt and a negative
prompt.  These strings can be passed directly into the standard
ComfyUI `CLIPTextEncode` node to condition a diffusion model.

Example usage inside ComfyUI:

    1. Search for `HumanPrompt` in the node menu and insert it into
       your workflow.
    2. Choose the desired demographic and physical options from the
       dropdowns or edit the clothing description.
    3. Connect the first string output (positive prompt) to the
       `Positive` input of a `CLIPTextEncode` node and the second
       output (negative prompt) to the `Negative` input.

Notes
-----
* The age groups all start at 18 years or older to avoid generating
  minors.  Please do not specify minors in your prompts.
* The `nudity` option merely toggles whether clothing descriptors are
  included.  It does not enforce any particular style of nudity; the
  overall goal of the workflow is to produce non‑sexual, anatomical
  depictions.
* Feel free to adapt the lists of options to suit your own
  conventions or to localize the terminology.
"""

class HumanPrompt:
    """Constructs positive and negative prompts for realistic human generation."""

    # Display category under which the node appears in the add‑node menu
    CATEGORY = "Prompt Helpers"

    @classmethod
    def INPUT_TYPES(cls):
        """Defines the user‑visible inputs for this node.

        Returns
        -------
        dict
            A dictionary mapping ``required`` and ``optional`` inputs to
            tuples describing the input type and any additional
            parameters.  See the ComfyUI documentation for details on
            allowed datatypes.
        """
        return {
            "required": {
                # Drop‑down menus defined by lists of strings create
                # COMBO widgets in the UI.  The first option is the
                # default selection.
                "gender": ([
                    "female",
                    "male",
                    "androgynous",
                    "non‑binary"
                ], {}),
                "ethnicity": ([
                    "African descent",
                    "Asian descent",
                    "European descent",
                    "Hispanic/Latin descent",
                    "Middle Eastern descent",
                    "Indigenous descent",
                    "Mixed/other"
                ], {}),
                "age_group": ([
                    "18‑25",
                    "26‑35",
                    "36‑50",
                    "50+"
                ], {}),
                "height": ([
                    "short",
                    "average height",
                    "tall"
                ], {}),
                "body_type": ([
                    "slim",
                    "average",
                    "athletic/muscular",
                    "plus‑size"
                ], {}),
                "muscle_definition": ([
                    "low",
                    "medium",
                    "high"
                ], {}),
                "nudity": ([
                    "clothed",
                    "nude"
                ], {}),
                # Freeform clothing description when the subject is
                # clothed.  Ignored if nudity is set to "nude".
                "clothing_style": ("STRING", {"default": "casual wear"}),
                "studio_lighting": ([
                    "yes",
                    "no"
                ], {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "generate_prompts"

    def generate_prompts(
        self,
        gender: str,
        ethnicity: str,
        age_group: str,
        height: str,
        body_type: str,
        muscle_definition: str,
        nudity: str,
        clothing_style: str,
        studio_lighting: str,
    ):
        """Generate positive and negative prompt strings based on user input.

        Parameters
        ----------
        gender : str
            The gender descriptor (e.g. "female", "male").
        ethnicity : str
            The ethnic background descriptor.
        age_group : str
            Age range of the subject (must start at 18+).
        height : str
            Height descriptor (short, average height, tall).
        body_type : str
            Body shape descriptor (slim, average, athletic/muscular, plus‑size).
        muscle_definition : str
            Degree of muscular definition (low, medium, high).
        nudity : str
            Whether the subject is clothed or nude.  Only non‑sexual nudity is
            permitted.
        clothing_style : str
            Free text description of clothing.  Ignored if nude.
        studio_lighting : str
            Whether to emphasize studio lighting in the prompt.

        Returns
        -------
        tuple[str, str]
            A 2‑tuple containing the positive prompt and the negative prompt.
        """
        # Build the descriptor for the subject's physical appearance.
        appearance_parts = []
        # Add height and body type descriptors
        if height != "average height":
            appearance_parts.append(height)
        appearance_parts.append(body_type)
        # Muscle description
        muscle_map = {
            "low": "subtle muscle definition",
            "medium": "moderate muscle definition",
            "high": "high muscle definition"
        }
        appearance_parts.append(muscle_map.get(muscle_definition, "moderate muscle definition"))
        appearance_desc = ", ".join(appearance_parts)
        # Build the clothing descriptor
        if nudity == "nude":
            clothing_desc = "nude, full‑body anatomy study"
        else:
            clothing_desc = f"wearing {clothing_style}" if clothing_style.strip() else "fully clothed"
        # Studio lighting descriptor
        lighting_desc = "studio lighting" if studio_lighting == "yes" else "natural lighting"
        # Assemble the positive prompt
        positive_prompt = (
            f"full‑body photograph of a {appearance_desc} {gender} of {ethnicity}, "
            f"aged {age_group}, {clothing_desc}, arms relaxed at sides, standing upright in a studio "
            f"with {lighting_desc}. Highly realistic, detailed skin texture with pores and fine anatomy, "
            f"photographic quality, high resolution"
        )
        # Negative prompt to discourage unwanted artefacts and styles
        negative_prompt = (
            "cartoon, CGI, illustration, anime, painting, drawing, unrealistic, disproportionate limbs, "
            "extra limbs, deformed hands, distorted anatomy, blurry, low quality, sexual content, NSFW"
        )
        return (positive_prompt, negative_prompt)

NODE_CLASS_MAPPINGS = {
    "HumanPrompt": HumanPrompt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "HumanPrompt": "Human Prompt"
}
